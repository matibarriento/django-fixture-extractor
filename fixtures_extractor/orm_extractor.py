import json
import logging
from pathlib import Path

from django.apps import apps

from fixtures_extractor.encoders import EnhancedDjangoJSONEncoder

logger = logging.getLogger("extract_fixture")


class ORMExtractor:
    def get_records(self, app_model: str, filter_key: str, filter_value: str):
        # noinspection PyPep8Naming
        Model = apps.get_model(app_model)
        fields = self.get_fields(Model)

        records = Model.objects.all()

        if filter_key:
            records = records.filter(**{filter_key: filter_value}).all()

        return records.values(*fields)

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

    def get_all_model_attributes(self, Model):
        return (
            self.get_fields(Model)
            + self.get_many_to_many_relations(Model)
            + self.get_reverse_relations(Model)
        )

    def get_fields(self, Model):
        return [field.name for field in Model._meta.fields]

    def get_many_to_many_relations(self, Model):
        return [m2m.name for m2m in Model._meta.many_to_many]

    def get_reverse_relations(self, Model):
        return [
            relation.get_accessor_name() for relation in Model._meta.related_objects
        ]
