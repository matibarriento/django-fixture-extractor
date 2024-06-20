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
        pass

    def handle(self, *args, **options):
        pass
