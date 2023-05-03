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

logger = logging.getLogger('')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(
    logging.Formatter('%(name)s - %(levelname)s - %(message)s')
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

    def __init__(self, stdout=None, stderr=None, no_color=False):
        self.output_file_prefix = 1
        super().__init__(stdout, stderr, no_color)

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

        for model, schema in schema_config.items():
            if model.startswith("."):
                continue

            for primary_id in primary_ids:
                primary_output_dir = output_dir.joinpath(f"{model.lower()}_{primary_id}")
                primary_output_dir.mkdir(parents=True, exist_ok=True)

                self.process_schema(
                    schema=schema,
                    filter_value=primary_id,
                    output_dir=primary_output_dir,
                )
                self.output_file_prefix = 1

    def process_schema(self, schema, filter_value, output_dir):
        app_model = schema["model_name"]
        filter_key = schema.get("filter_key", None)

        logger.info(app_model)

        self.dump_fixture(
            app_model=app_model,
            filter_key=filter_key,
            filter_value=filter_value,
            output_dir=output_dir,
        )

        if "parent" in schema:
            self.process_schema(
                schema=schema["parent"],
                filter_value=filter_value,
                output_dir=output_dir,
            )

        if "dependencies" in schema:
            for _, dep_schema in schema["dependencies"].items():
                self.process_schema(
                    schema=dep_schema,
                    filter_value=filter_value,
                    output_dir=output_dir,
                )

    def dump_fixture(self, app_model, filter_key, filter_value, output_dir):
        records = self.get_records(
            app_model=app_model, filter_key=filter_key,
            filter_value=filter_value
        )
        output_file = self.make_output_name(
            app_model, output_dir, self.output_file_prefix
        )
        self.dump_records(
            app_model=app_model, output_file=output_file, records=records
        )

        self.output_file_prefix += 1

    def make_output_name(self, app_model, output_dir, prefix):
        return output_dir.joinpath(f"{prefix}_{app_model}.json")

    def get_records(self, app_model, filter_key, filter_value):
        # noinspection PyPep8Naming
        Model = apps.get_model(app_model)
        fields = self.get_all_fields(Model)

        records = Model.objects.all()

        if filter_key:
            records = records.filter(**{filter_key: filter_value}).all()

        return records.values(*fields)

    def dump_records(self, app_model, output_file, records):
        dump_structure = self.get_dump_structure(app_model, records)
        result = json.dumps(
            dump_structure, cls=EnhancedDjangoJSONEncoder, indent=4
        )
        logger.info(output_file)
        with open(output_file, "w+") as output:
            output.write(result)

    def get_dump_structure(self, app_model, records):
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

    def get_all_fields(self, Model):
        return [field.name for field in Model._meta.fields]
