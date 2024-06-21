from pathlib import Path
import pytest
from django.core.management import call_command

from tests.management.commands.utils import (
    date_repr,
    get_json_from_file,
)
from tests.testproject.testapp.factories import (
    RecordLabelFactory,
    AlbumFactory,
    ArtistFactory,
)

pytestmark = [pytest.mark.django_db]


def test_run_command_only_simple_model(tmp_path):
    record_label_1 = RecordLabelFactory.create()
    RecordLabelFactory.create()

    output_dir = tmp_path / "fixtures"
    output_dir.mkdir()

    options = {
        "app": "testapp",
        "model": "recordlabel",
        "output_dir": output_dir,
    }
    call_command("extract_fixture", record_label_1.id, **options)

    output_file = Path(output_dir).joinpath(
        f"recordlabel_{record_label_1.id}/testapp.recordlabel.json"
    )
    expected_json = [
        {
            "model": "testapp.recordlabel",
            "fields": {
                "id": 1,
                "name": record_label_1.name,
            },
        }
    ]

    output_json = get_json_from_file(output_file)

    assert output_json == expected_json


def test_run_command_multiple_related_model(tmp_path):
    record_label = RecordLabelFactory.create()
    artist = ArtistFactory.create()
    album = AlbumFactory.create(record_label=record_label, artist=artist)

    output_dir = tmp_path / "fixtures"
    output_dir.mkdir()

    options = {
        "app": "testapp",
        "model": "recordlabel",
        "output_dir": output_dir,
    }
    call_command("extract_fixture", record_label.id, **options)

    output_file = Path(output_dir).joinpath(
        f"recordlabel_{record_label.id}/testapp.recordlabel.json"
    )
    expected_json = [
        {
            "model": "testapp.recordlabel",
            "fields": {
                "id": 1,
                "name": record_label.name,
            },
        },
        {
            "model": "testapp.album",
            "fields": {
                "id": album.id,
                "artist": album.artist.id,
                "name": album.name,
                "release_date": date_repr(album.release_date),
                "record_label": record_label.id,
            },
        },
        {
            "model": "testapp.artist",
            "fields": {
                "id": artist.id,
                "first_name": artist.first_name,
                "last_name": artist.last_name,
                "instrument": artist.instrument,
            },
        },
    ]

    # TODO Remove when dupes registry is implemented
    expected_json.extend(
        [
            {
                "model": "testapp.album",
                "fields": {
                    "id": album.id,
                    "artist": album.artist.id,
                    "name": album.name,
                    "release_date": date_repr(album.release_date),
                    "record_label": record_label.id,
                },
            },
            {
                "model": "testapp.recordlabel",
                "fields": {
                    "id": 1,
                    "name": record_label.name,
                },
            },
        ]
    )

    expected_json = sorted(expected_json, key=lambda x: x["model"])

    output_json = sorted(get_json_from_file(output_file), key=lambda x: x["model"])

    assert output_json == expected_json
