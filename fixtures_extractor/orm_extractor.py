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
        model = apps.get_model(app_model)
        fields = self.get_model_fields(app_model=app_model)
        relation_fields = self.get_model_declared_relations(app_model=app_model)
        field_names = [field.field_name for field in fields]
        relation_field_names = [field.field_name for field in relation_fields]

        records = model.objects.all()

        if filter_key:
            records = records.filter(**{filter_key: filter_value}).all()

        return records.values(*field_names, *relation_field_names)

    def dump_records(self, records: list, output_file: Path):
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

    def get_many_to_many_relations(self, app_model) -> list[ModelFieldMetaDTO]:
        return [
            field
            for field in self.get_all_fields(app_model=app_model)
            if field.field_type == FieldType.many_to_many
        ]

    def get_reverse_relations(self, app_model) -> list[ModelFieldMetaDTO]:
        return [
            field
            for field in self.get_all_fields(app_model=app_model)
            if field.field_type == FieldType.reverse_foreign_key
        ]

    def get_model_declared_relations(self, app_model) -> list[ModelFieldMetaDTO]:
        return [
            field
            for field in self.get_all_fields(app_model=app_model)
            if field.is_model_declared and field.field_type != FieldType.field
        ]

    def get_model_target_relations(self, app_model) -> list[ModelFieldMetaDTO]:
        return [
            field
            for field in self.get_all_fields(app_model=app_model)
            if not field.is_model_declared and field.field_type != FieldType.field
        ]
