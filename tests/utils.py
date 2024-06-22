import json
from datetime import date, datetime
from pathlib import Path

from django.core.management import call_command


def date_repr(field_date: date, format: str = "%Y-%m-%d"):
    return field_date.strftime(format)


def datetime_repr(field_datetime: datetime):
    truncated_microseconds = field_datetime.strftime("%f")[:3]
    return field_datetime.strftime("%Y-%m-%dT%H:%M:%S.") + truncated_microseconds + "Z"


def assert_fixture_output_file(output_file: Path, expected_json: list):
    assert output_file.exists(), list(output_file.parent.glob("*"))

    with open(output_file, "r") as output_content:
        output_json = json.load(output_content)

    assert output_json == expected_json, (output_json, expected_json)

    call_command("loaddata", output_file)


def get_json_from_file(file_path: Path):
    assert file_path.exists(), list(file_path.parent.glob("*"))

    with open(file_path, "r") as file_content:
        return json.load(file_content)
