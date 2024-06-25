from curses.ascii import islower
import logging
from math import log
from shlex import join
import sys
from pathlib import Path
from typing import List

from django.core.management.base import BaseCommand

from fixtures_extractor.extra_logging_formatter import ExtraFormatter
from fixtures_extractor.orm_extractor import ORMExtractor

logger = logging.getLogger("extract_fixture")
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(ExtraFormatter("%(name)s - %(levelname)s - %(message)s"))
logger.addHandler(console)


VERBOSITY = {
    0: logging.ERROR,
    1: logging.WARN,
    2: logging.INFO,
    3: logging.DEBUG,
}


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
        logger.setLevel(VERBOSITY[options.get("verbosity", 0)])

        app_name = options.get("app")
        model_name = options.get("model")
        output_dir = Path(options.get("output_dir"))

        logger.info(
            f"Extracting fixtures for {app_name}.{model_name} into '{output_dir}' path"
        )

        filter_key = "id"
        primary_ids: List = options.get("primary_ids")
        logger.info(f"Filtering by {filter_key}={primary_ids}")

        if not app_name.islower() or not model_name.islower():
            logger.warning(
                "App and model names should be lowercase, they will be lowercased for you"
            )

        app_name = app_name.lower()
        model_name = model_name.lower()
        full_model_name = f"{app_name}.{model_name}"
        logger.debug(f"Full model name: {full_model_name}")

        for primary_id in primary_ids:
            try:
                logger.debug(
                    f"Processing {full_model_name} with {filter_key}={primary_id}"
                )
                primary_output_dir = output_dir.joinpath(
                    f"{model_name.lower()}_{primary_id}"
                )
                primary_output_dir.mkdir(parents=True, exist_ok=True)
                output_file = primary_output_dir.joinpath(f"{full_model_name}.json")

                records = self.process_fields(
                    full_model_name=full_model_name,
                    filter_key=filter_key,
                    filter_value=str(primary_id),
                    history=[],
                    origin=full_model_name,
                )

                orm_extractor.dump_records(output_file=output_file, records=records)
                logger.info(f"File {output_file} saved")
            except Exception as ex:
                logger.error(
                    f"Error processing {full_model_name} with {filter_key}={primary_id}"
                )
                logger.debug(ex, exc_info=True)

    def process_fields(
        self,
        full_model_name: str,
        filter_key: str,
        filter_value: str,
        history: List,
        origin: str,
    ) -> list:
        navigation_msg = f"navigating form {origin} to {full_model_name} with {filter_key}={filter_value}"

        if (origin, full_model_name, filter_key, filter_value) in history:
            logger.debug(f"Skipped {navigation_msg}, was already processed")
            return []

        logger.info(f"Processing {navigation_msg}")
        history.append((origin, full_model_name, filter_key, filter_value))

        schema_records = []

        base_model_records = orm_extractor.get_records(
            app_model=full_model_name, filter_key=filter_key, filter_value=filter_value
        )

        if len(base_model_records) == 0:
            logger.debug(f"No records found for {full_model_name}")
            return []

        jsonfy_records = orm_extractor.build_records(
            app_model=full_model_name, records=base_model_records
        )
        schema_records.extend(jsonfy_records)

        one_relation_declared_fields = orm_extractor.get_model_declared_one_relations(
            app_model=full_model_name
        )
        logger.debug(f"Found {len(one_relation_declared_fields)} one declared fields")

        many_relation_declared_fields = orm_extractor.get_model_declared_many_relations(
            app_model=full_model_name
        )
        logger.debug(f"Found {len(many_relation_declared_fields)} many declared fields")

        target_relation_fields = orm_extractor.get_model_target_relations(
            app_model=full_model_name
        )
        logger.debug(f"Found {len(target_relation_fields)} target fields")

        for record in base_model_records:
            logger.debug("Processing one relation fields")
            for one_declared_field in one_relation_declared_fields:
                full_name = (
                    f"{one_declared_field.app_name}.{one_declared_field.model_name}"
                )
                one_declared_records = self.process_fields(
                    full_model_name=full_name,
                    filter_key="id",
                    filter_value=record[one_declared_field.field_name],
                    history=history,
                    origin=full_model_name,
                )
                schema_records.extend(one_declared_records)

            logger.debug("Processing many relation fields")
            for many_declared_field in many_relation_declared_fields:
                full_name = (
                    f"{many_declared_field.app_name}.{many_declared_field.model_name}"
                )

                for filter_value in record[many_declared_field.field_name]:
                    many_declared_records = self.process_fields(
                        full_model_name=full_name,
                        filter_key="id",
                        filter_value=filter_value,
                        history=history,
                        origin=full_model_name,
                    )
                    schema_records.extend(many_declared_records)

            logger.debug("Processing target relation fields")
            for target_field in target_relation_fields:
                full_name = f"{target_field.app_name}.{target_field.model_name}"
                target_records = self.process_fields(
                    full_model_name=full_name,
                    filter_key=target_field.field_name,
                    filter_value=record["id"],
                    history=history,
                    origin=full_model_name,
                )
                schema_records.extend(target_records)

        return schema_records
