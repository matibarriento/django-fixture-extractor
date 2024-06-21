"""
Based on https://github.com/ascaliaio/django-dumpdata-one
"""

import logging
from pathlib import Path

from django.core.management.base import BaseCommand

from fixtures_extractor.extra_logging_formatter import ExtraFormatter
from fixtures_extractor.orm_extractor import ORMExtractor

logger = logging.getLogger("extract_fixture")
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
            required=True,
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
        full_model_name = f"{app_name}.{model_name}"

        filter_key = "id"

        primary_ids = options.get("primary_ids")
        output_dir = Path(options.get("output_dir"))

        for primary_id in primary_ids:
            primary_output_dir = output_dir.joinpath(
                f"{model_name.lower()}_{primary_id}"
            )
            primary_output_dir.mkdir(parents=True, exist_ok=True)
            output_file = primary_output_dir.joinpath(f"{full_model_name}.json")

            records = self.process_declared_fields(
                full_model_name=full_model_name,
                filter_key=filter_key,
                filter_value=str(primary_id),
                history=[],
                origin=full_model_name,
            )

            orm_extractor.dump_records(output_file=output_file, records=records)

    def process_declared_fields(
        self,
        full_model_name: str,
        filter_key: str,
        filter_value: str,
        history: list,
        origin: str,
    ) -> list:
        print(history)
        if (origin, full_model_name, filter_key, filter_value) in history:
            return []

        schema_records = []
        history.append((origin, full_model_name, filter_key, filter_value))

        base_model_records = orm_extractor.get_records(
            app_model=full_model_name, filter_key=filter_key, filter_value=filter_value
        )
        jsonfy_records = orm_extractor.build_records(
            app_model=full_model_name, records=base_model_records
        )
        schema_records.extend(jsonfy_records)

        declared_fields = orm_extractor.get_model_declared_relations(
            app_model=full_model_name
        )
        target_fields = orm_extractor.get_model_target_relations(
            app_model=full_model_name
        )

        for record in base_model_records:
            for declared_field in declared_fields:
                full_name = f"{declared_field.app_name}.{declared_field.model_name}"
                dependency_records = self.process_declared_fields(
                    full_model_name=full_name,
                    filter_key="id",
                    filter_value=record[declared_field.field_name],
                    history=history,
                    origin=full_model_name,
                )
                schema_records.extend(dependency_records)

            for target_field in target_fields:
                full_name = f"{target_field.app_name}.{target_field.model_name}"
                dependency_records = self.process_declared_fields(
                    full_model_name=full_name,
                    filter_key=target_field.field_name,
                    filter_value=record["id"],
                    history=history,
                    origin=full_model_name,
                )
                schema_records.extend(dependency_records)

        return schema_records
