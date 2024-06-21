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

        model = self.get_model(app_model=app_model)
        records = model.objects.all()

        if filter_key:
            records = records.filter(**{filter_key: filter_value}).all()

        return records.values(*field_names)

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

    def dump_records(self, records: list, output_file: Path):
        logger.info(output_file)
        jsonfy_records = json.dumps(records, cls=EnhancedDjangoJSONEncoder, indent=4)
        with open(output_file, "w+") as output:
            output.writelines(jsonfy_records)

    def get_model(self, app_model: str):
        return apps.get_model(app_label=app_model)

    def get_all_fields(self, Model):
        return sorted(
            [ModelFieldMetaDTO.build(field) for field in Model._meta.get_fields()]
        )

    def get_model_fields(self, app_model) -> list[ModelFieldMetaDTO]:
        model = self.get_model(app_model=app_model)
        return [
            field
            for field in self.get_all_fields(Model=model)
            if field.field_type == FieldType.field
        ]

    def get_many_to_many_relations(self, Model) -> list[ModelFieldMetaDTO]:
        return [
            field
            for field in self.get_all_fields(Model)
            if field.field_type == FieldType.many_to_many
        ]

    def get_reverse_relations(self, Model) -> list[ModelFieldMetaDTO]:
        return [
            field
            for field in self.get_all_fields(Model)
            if field.field_type == FieldType.reverse_foreign_key
        ]

    def get_model_declared_relations(self, app_model) -> list[ModelFieldMetaDTO]:
        model = apps.get_model(app_model)

        return [
            field
            for field in self.get_all_fields(model)
            if field.is_model_declared and field.field_type != FieldType.field
        ]

    def get_model_target_relations(self, app_model) -> list[ModelFieldMetaDTO]:
        model = apps.get_model(app_model)

        return [
            field
            for field in self.get_all_fields(model)
            if not field.is_model_declared and field.field_type != FieldType.field
        ]
