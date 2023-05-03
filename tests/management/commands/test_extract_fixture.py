import json
from datetime import date
from pathlib import Path

import pytest
from django.core.management import call_command

from tests.factories import MusicianFactory, AlbumFactory

pytestmark = [pytest.mark.django_db]

SCHEMA_DIR = "tests/management/schemas"


def _date_repr(field_date: date):
    return field_date.strftime("%Y-%m-%d")


def _assert_fixture_output_file(output_file: Path, expected_json: list):
    assert output_file.exists(), list(output_file.parent.glob("*"))

    with open(output_file, "r") as output_content:
        output_json = json.load(output_content)

    assert output_json == expected_json

    call_command('loaddata', output_file)


def test_simple_model_musician(tmp_path):
    musician = MusicianFactory.create(id=1)
    MusicianFactory.create(id=2)

    output_dir = tmp_path / "fixtures"
    output_dir.mkdir()

    options = {
        "schema": Path(SCHEMA_DIR).joinpath("simple_model_musicians.yaml"),
        "output_dir": output_dir
    }
    call_command('extract_fixture', "1", **options)

    output_file = Path(output_dir).joinpath("musician_1/1_testapp.musician.json")
    expected_json = [
        {
            'model': 'testapp.musician',
            'fields': {
                'id': 1,
                'first_name': musician.first_name,
                'last_name': musician.last_name,
                'instrument': musician.instrument
            }
        }
    ]

    _assert_fixture_output_file(output_file, expected_json)


def test_related_musician_and_album(tmp_path):
    musician = MusicianFactory.create(id=1)
    album = AlbumFactory.create(id=1, artist=musician)

    output_dir = tmp_path / "fixtures"
    output_dir.mkdir()

    options = {
        "schema": Path(SCHEMA_DIR).joinpath("related_musician_and_album.yaml"),
        "output_dir": output_dir
    }
    call_command('extract_fixture', "1", **options)

    output_file = Path(output_dir).joinpath("album_1/1_testapp.album.json")

    expected_json = [
        {
            'model': 'testapp.album',
            'fields': {
                'id': album.id,
                'artist': album.artist_id,
                'name': album.name,
                'release_date': _date_repr(album.release_date)
            }
        }
    ]

    _assert_fixture_output_file(output_file, expected_json)

    output_file = Path(output_dir).joinpath("album_1/2_testapp.musician.json")

    expected_json = [
        {
            'model': 'testapp.musician',
            'fields': {
                'id': 1,
                'first_name': musician.first_name,
                'last_name': musician.last_name,
                'instrument': musician.instrument
            }
        }
    ]

    _assert_fixture_output_file(output_file, expected_json)
