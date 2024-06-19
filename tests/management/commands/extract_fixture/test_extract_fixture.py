from pathlib import Path

import pytest
from django.core.management import call_command

from tests.management.commands.utils import assert_fixture_output_file, date_repr
from tests.testproject.testapp.factories import AlbumFactory, MusicianFactory

pytestmark = [pytest.mark.django_db]

SCHEMA_DIR = "tests/management/schemas"


def test_simple_model_musician(tmp_path):
    musician = MusicianFactory.create(id=1)
    MusicianFactory.create(id=2)

    output_dir = tmp_path / "fixtures"
    output_dir.mkdir()

    options = {
        "schema": Path(SCHEMA_DIR).joinpath("simple_model_musicians.yaml"),
        "output_dir": output_dir,
    }
    call_command("extract_fixture", "1", **options)

    output_file = Path(output_dir).joinpath("musician_1/testapp.musician.json")
    expected_json = [
        {
            "model": "testapp.musician",
            "fields": {
                "id": 1,
                "first_name": musician.first_name,
                "last_name": musician.last_name,
                "instrument": musician.instrument,
            },
        }
    ]

    assert_fixture_output_file(output_file, expected_json)


def test_related_musician_and_album(tmp_path):
    musician = MusicianFactory.create(id=1)
    album = AlbumFactory.create(id=1, artist=musician)

    output_dir = tmp_path / "fixtures"
    output_dir.mkdir()

    options = {
        "schema": Path(SCHEMA_DIR).joinpath("related_musician_and_album.yaml"),
        "output_dir": output_dir,
    }
    call_command("extract_fixture", "1", **options)

    output_file = Path(output_dir).joinpath("album_1/testapp.album.json")

    expected_json = [
        {
            "model": "testapp.album",
            "fields": {
                "id": album.id,
                "artist": album.artist_id,
                "name": album.name,
                "release_date": date_repr(album.release_date),
            },
        },
        {
            "model": "testapp.musician",
            "fields": {
                "id": musician.id,
                "first_name": musician.first_name,
                "last_name": musician.last_name,
                "instrument": musician.instrument,
            },
        },
    ]

    assert_fixture_output_file(output_file, expected_json)


def test_one_file(tmp_path):
    musician = MusicianFactory.create(id=1)
    album = AlbumFactory.create(id=1, artist=musician)

    output_dir = tmp_path / "fixtures"
    output_dir.mkdir()

    options = {
        "schema": Path(SCHEMA_DIR).joinpath("related_musician_and_album.yaml"),
        "output_dir": output_dir,
    }
    call_command("extract_fixture", "1", **options)

    output_fixture_dir = Path(output_dir).joinpath("album_1")

    assert len(list(output_fixture_dir.glob("*.json"))) == 1

    output_file = output_fixture_dir.joinpath("testapp.album.json")

    expected_json = [
        {
            "model": "testapp.album",
            "fields": {
                "id": album.id,
                "artist": album.artist_id,
                "name": album.name,
                "release_date": date_repr(album.release_date),
            },
        },
        {
            "model": "testapp.musician",
            "fields": {
                "id": musician.id,
                "first_name": musician.first_name,
                "last_name": musician.last_name,
                "instrument": musician.instrument,
            },
        },
    ]

    assert_fixture_output_file(output_file, expected_json)
