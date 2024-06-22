import json
import logging
from pathlib import Path

from django.apps import apps

from fixtures_extractor.dtos import ModelFieldMetaDTO
from fixtures_extractor.encoders import EnhancedDjangoJSONEncoder
from fixtures_extractor.enums import FieldType

logger = logging.getLogger()


class ORMExtractor:
    def get_records(self, app_model: str, filter_key: str, filter_value: str):
        fields = self.get_model_fields(app_model=app_model)
        field_names = [field.field_name for field in fields]

        one_relation_fields = self.get_model_declared_one_relations(app_model=app_model)
        one_relation_field_names = [field.field_name for field in one_relation_fields]

        many_to_many_fields = self.get_model_declared_many_relations(
            app_model=app_model
        )
        many_to_many_field_names = [field.field_name for field in many_to_many_fields]

        model = apps.get_model(app_model)
        records = model.objects.all()

        if filter_key:
            records = records.filter(**{filter_key: filter_value}).all()

        base_record_values = list(
            records.values(
                *field_names,
                *one_relation_field_names,
            )
        )

        for index, record in enumerate(records):
            for m2m_field_name in many_to_many_field_names:
                base_record_values[index][m2m_field_name] = list(
                    getattr(record, m2m_field_name).values_list("id", flat=True)
                )

        return base_record_values

    def dump_records(self, records: list, output_file: Path):
        def record_key(record):
            return (record["model"], record["fields"]["id"])

        records = list({record_key(record): record for record in records}.values())

        logger.info(output_file)

        jsonfy_records = json.dumps(records, cls=EnhancedDjangoJSONEncoder, indent=4)
        with open(output_file, "w+") as output:
            output.writelines(jsonfy_records)

    def build_records(self, app_model: str, records: list) -> list:
        results = []
        for item in records:
            values = {}
            for key, value in item.items():
                if key != "pk":
                    values[key] = value

            item_structure = {"model": app_model, "fields": values}
            results.append(item_structure)

        return results

    def get_all_fields(self, app_model):
        model = apps.get_model(app_label=app_model)
        return sorted(
            [ModelFieldMetaDTO.build(field=field) for field in model._meta.get_fields()]
        )

    def get_model_fields(self, app_model) -> list[ModelFieldMetaDTO]:
        return [
            field
            for field in self.get_all_fields(app_model=app_model)
            if field.field_type == FieldType.field
        ]

    def get_model_declared_many_relations(self, app_model) -> list[ModelFieldMetaDTO]:
        return [
            field
            for field in self.get_all_fields(app_model=app_model)
            if field.is_model_declared and field.field_type == FieldType.many_to_many
        ]

    def get_model_declared_one_relations(self, app_model) -> list[ModelFieldMetaDTO]:
        return [
            field
            for field in self.get_all_fields(app_model=app_model)
            if field.is_model_declared
            and field.field_type in [FieldType.one_to_one, FieldType.foreign_key]
        ]

    def get_model_target_relations(self, app_model) -> list[ModelFieldMetaDTO]:
        return [
            field
            for field in self.get_all_fields(app_model=app_model)
            if not field.is_model_declared and field.field_type != FieldType.field
        ]
