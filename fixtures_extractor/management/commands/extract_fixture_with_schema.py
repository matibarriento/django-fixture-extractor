"""
Based on https://github.com/ascaliaio/django-dumpdata-one
"""

import argparse
import logging
from pathlib import Path

import yaml
from django.core.management.base import BaseCommand

from fixtures_extractor.extra_logging_formatter import ExtraFormatter
from fixtures_extractor.orm_extractor import ORMExtractor

logger = logging.getLogger("extract_fixture_with_schema")
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(ExtraFormatter("%(name)s - %(levelname)s - %(message)s"))
logger.addHandler(console)


orm_extractor = ORMExtractor()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "primary_ids",
            type=int,
            nargs="+",
            help="Primary ids of the start model to dump",
        )
        parser.add_argument(
            "-s",
            "--schema",
            type=argparse.FileType("r"),
            help="Schema of the models to dump",
        )
        parser.add_argument(
            "-d",
            "--output_dir",
            type=str,
            default="fixtures",
            help="Output dir for all the resulted fixtures",
        )

    def handle(self, *args, **options):
        schema_file = options.get("schema")

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
                primary_output_dir = output_dir.joinpath(
                    f"{model.lower()}_{primary_id}"
                )
                primary_output_dir.mkdir(parents=True, exist_ok=True)
                output_file = primary_output_dir.joinpath(f"{initial_app_model}.json")

                records = self.process_schema(
                    schema=schema,
                    filter_value=primary_id,
                    output_dir=primary_output_dir,
                )

                orm_extractor.dump_records(output_file=output_file, records=records)

    def process_schema(self, schema: dict, filter_value: str, output_dir: Path) -> list:
        schema_records = []
        app_model = schema["model_name"]
        filter_key = schema.get("filter_key", None)

        logger.info(app_model)

        base_model_records = orm_extractor.get_records(
            app_model=app_model, filter_key=filter_key, filter_value=filter_value
        )
        jsonfy_records = orm_extractor.build_records(app_model, base_model_records)
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
