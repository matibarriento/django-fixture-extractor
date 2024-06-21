"""
Based on https://github.com/ascaliaio/django-dumpdata-one
"""

import logging
from pathlib import Path

from django.apps import apps
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
            "-a",
            "--app",
            type=str,
            help="App of the start model to dump",
        )
        parser.add_argument(
            "-m",
            "--model",
            type=str,
            help="Name of the start model to dump",
        )
        parser.add_argument(
            "primary_ids",
            type=int,
            nargs="+",
            help="Primary ids of the start model to dump",
        )
        parser.add_argument(
            "-d",
            "--output_dir",
            type=str,
            default="fixtures",
            help="Output dir for all the resulted fixtures",
        )

    def handle(self, *args, **options):
        app_name = options.get("app")
        model_name = options.get("model")
        full_model_name = f'{app_name}.{model_name}'

        filter_key = 'id'

        primary_ids = options.get("primary_ids")
        output_dir = Path(options.get("output_dir"))

        for primary_id in primary_ids:
            primary_output_dir = output_dir.joinpath(
                f"{model_name.lower()}_{primary_id}"
            )
            primary_output_dir.mkdir(parents=True, exist_ok=True)
            output_file = primary_output_dir.joinpath(f'{full_model_name}.json')

            records = self.process_schema(
                full_model_name=full_model_name,
                filter_key=filter_key,
                filter_value=primary_id,
                output_dir=primary_output_dir,
            )

            orm_extractor.dump_records(output_file=output_file, records=records)

    def process_schema(self, full_model_name: str, filter_key: str, filter_value: str, output_dir: Path) -> list:
        schema_records = []

        logger.info(full_model_name)

        base_model_records = orm_extractor.get_records(
            app_model=full_model_name, filter_key=filter_key, filter_value=filter_value
        )
        jsonfy_records = orm_extractor.build_records(full_model_name, base_model_records)
        schema_records.extend(jsonfy_records)

        Model = apps.get_model(full_model_name)

        for reverse_relation in Model._meta.related_objects:
            reverse_app_name = reverse_relation.related_model._meta.app_label
            reverse_model_name = reverse_relation.related_model._meta.model_name

            for record in base_model_records:
                dependency_records = self.process_schema(
                    full_model_name=f'{reverse_app_name}.{reverse_model_name}',
                    filter_key=reverse_relation.field.name,
                    filter_value=record['id'],
                    output_dir=output_dir,
                )
                schema_records.extend(dependency_records)

        return schema_records
