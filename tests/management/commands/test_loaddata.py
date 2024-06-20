import json

import pytest
from django.core.management import call_command
from django.core.serializers.base import DeserializationError

from tests.testproject.testapp.factories import ArtistFactory, AlbumFactory
from tests.management.commands.utils import date_repr
from tests.testproject.testapp.models import Artist, Album

pytestmark = [pytest.mark.django_db]


def test_fixture_load(tmp_path):
    fixture_file = tmp_path / "fixture.json"

    expected_artist = ArtistFactory.build(id=1)

    # Sanity check
    assert not Artist.objects.filter(id=expected_artist.id).exists()

    fixture_json = [
        {
            "model": "testapp.artist",
            "fields": {
                "id": expected_artist.id,
                "first_name": expected_artist.first_name,
                "last_name": expected_artist.last_name,
                "instrument": expected_artist.instrument,
            },
        }
    ]

    with open(fixture_file, "w") as fixture_stream:
        json.dump(fixture_json, fixture_stream)

    call_command("loaddata", fixture_file)

    artist = Artist.objects.get(id=expected_artist.id)

    assert artist.id == expected_artist.id
    assert artist.first_name == expected_artist.first_name
    assert artist.last_name == expected_artist.last_name
    assert artist.instrument == expected_artist.instrument


def test_complex_fixture(tmp_path):
    fixture_file = tmp_path / "fixture.json"

    expected_artist = ArtistFactory.build(id=1)
    expected_album = AlbumFactory.build(id=1, artist=expected_artist)

    # Sanity check
    assert not Artist.objects.filter(id=expected_artist.id).exists()
    assert not Album.objects.filter(id=expected_album.id).exists()

    fixture_json = [
        {
            "model": "testapp.album",
            "fields": {
                "id": expected_album.id,
                "artist": expected_album.artist_id,
                "name": expected_album.name,
                "release_date": date_repr(expected_album.release_date),
            },
        },
        {
            "model": "testapp.artist",
            "fields": {
                "id": expected_artist.id,
                "first_name": expected_artist.first_name,
                "last_name": expected_artist.last_name,
                "instrument": expected_artist.instrument,
            },
        },
    ]

    with open(fixture_file, "w") as fixture_stream:
        json.dump(fixture_json, fixture_stream)

    call_command("loaddata", fixture_file)

    artist = Artist.objects.get(id=expected_artist.id)

    assert artist.id == expected_artist.id
    assert artist.first_name == expected_artist.first_name
    assert artist.last_name == expected_artist.last_name
    assert artist.instrument == expected_artist.instrument

    album = Album.objects.get(id=expected_album.id)

    assert album.artist == expected_artist
    assert album.name == expected_album.name
    assert album.release_date == expected_album.release_date


def test_corrupt_fixture_load(tmp_path):
    fixture_file = tmp_path / "fixture.json"

    assert not Artist.objects.exists()

    fixture_json = [
        {
            "model": "testapp.artist",
        }
    ]

    with open(fixture_file, "w") as fixture_stream:
        json.dump(fixture_json, fixture_stream)

    with pytest.raises(DeserializationError) as exc_info:
        call_command("loaddata", fixture_file)

    assert exc_info.value.args[0] == f"Problem installing fixture '{fixture_file}': "
    assert not Artist.objects.exists()
