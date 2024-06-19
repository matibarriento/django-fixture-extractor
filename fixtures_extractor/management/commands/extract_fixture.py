"""
Based on https://github.com/ascaliaio/django-dumpdata-one
"""
import argparse
import json
import logging
from enum import Enum
from pathlib import Path

import yaml
from django.apps import apps
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder

from fixtures_extractor.extra_logging_formatter import ExtraFormatter

logger = logging.getLogger('extract_fixture')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(
    ExtraFormatter('%(name)s - %(levelname)s - %(message)s')
)
logger.addHandler(console)


class EnhancedDjangoJSONEncoder(DjangoJSONEncoder):
    """Default DjangoJSONEncoder does not support Enum"""

    def default(self, o):
        if isinstance(o, Enum):
            # Currently support enum as value
            return o.value

        # Call super to continue with the default encoders
        return super().default(o)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'primary_ids',
            type=int,
            nargs="+",
            help="Primary ids of the start model to dump"
        )
        parser.add_argument(
            '-s',
            '--schema',
            type=argparse.FileType("r"),
            help="Schema of the models to dump"
        )
        parser.add_argument(
            '-d',
            '--output_dir',
            type=str,
            default="fixtures",
            help="Output dir for all the resulted fixtures"
        )

    def handle(self, *args, **options):

        schema_file = options.get('schema')

        assert Path(schema_file).exists(), f"Schema {schema_file} does not exists"

        with open(schema_file, "r") as schema_stream:
            schema_config = yaml.load(stream=schema_stream, Loader=yaml.SafeLoader)

        primary_ids = options.get("primary_ids")
        output_dir = Path(options.get("output_dir"))

        for primary_id in primary_ids:

            for model, schema in schema_config.items():
                if model.startswith("."):
                    continue

                initial_app_model = schema["model_name"]
                primary_output_dir = output_dir.joinpath(f"{model.lower()}_{primary_id}")
                primary_output_dir.mkdir(parents=True, exist_ok=True)
                output_file = primary_output_dir.joinpath(f"{initial_app_model}.json")

                records = self.process_schema(
                    schema=schema,
                    filter_value=primary_id,
                    output_dir=primary_output_dir,
                )

                self.dump_records(output_file=output_file, records=records)

    def process_schema(self, schema: dict, filter_value: str, output_dir: Path) -> list:
        schema_records = []
        app_model = schema["model_name"]
        filter_key = schema.get("filter_key", None)

        logger.info(app_model)

        base_model_records = self.get_records(
            app_model=app_model, filter_key=filter_key,
            filter_value=filter_value
        )
        jsonfy_records = self.build_records(app_model, base_model_records)
        schema_records.extend(jsonfy_records)

        if "parent" in schema:
            parent_records = self.process_schema(
                schema=schema["parent"],
                filter_value=filter_value,
                output_dir=output_dir,
            )
            schema_records.extend(parent_records)

        if "dependencies" in schema:
            for _, dep_schema in schema["dependencies"].items():
                dependency_records = self.process_schema(
                    schema=dep_schema,
                    filter_value=filter_value,
                    output_dir=output_dir,
                )
                schema_records.extend(dependency_records)

        return schema_records

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
        jsonfy_records = json.dumps(
            records, cls=EnhancedDjangoJSONEncoder, indent=4
        )
        with open(output_file, "w+") as output:
            output.writelines(jsonfy_records)

    def build_records(self, app_model: str, records: list) -> list:
        results = []
        for item in records:
            values = {}
            for key, value in item.items():
                if key != "pk":
                    values[key] = value

            item_structure = {
                "model": app_model,
                "fields": values
            }
            results.append(item_structure)

        return results

    def get_fields(self, Model):
        return [field.name for field in Model._meta.fields]

    def get_many_to_many(self, Model):
        return [m2m.name for m2m in Model._meta.many_to_many]
