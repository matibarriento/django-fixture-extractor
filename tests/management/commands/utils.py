import json
from datetime import date
from pathlib import Path

from django.core.management import call_command


def date_repr(field_date: date):
    return field_date.strftime("%Y-%m-%d")


def assert_fixture_output_file(output_file: Path, expected_json: list):
    assert output_file.exists(), list(output_file.parent.glob("*"))

    with open(output_file, "r") as output_content:
        output_json = json.load(output_content)

    assert output_json == expected_json, (output_json, expected_json)

    call_command('loaddata', output_file)
