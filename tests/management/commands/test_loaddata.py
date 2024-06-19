import json

import pytest
from django.core.management import call_command
from django.core.serializers.base import DeserializationError

from tests.testproject.testapp.factories import MusicianFactory, AlbumFactory
from tests.management.commands.utils import date_repr
from tests.testproject.testapp.models import Musician, Album

pytestmark = [pytest.mark.django_db]


def test_fixture_load(tmp_path):
    fixture_file = tmp_path / "fixture.json"

    expected_musician = MusicianFactory.build(id=1)

    # Sanity check
    assert not Musician.objects.filter(id=expected_musician.id).exists()

    fixture_json = [
        {
            'model': 'testapp.musician',
            'fields': {
                'id': expected_musician.id,
                'first_name': expected_musician.first_name,
                'last_name': expected_musician.last_name,
                'instrument': expected_musician.instrument
            }
        }
    ]

    with open(fixture_file, "w") as fixture_stream:
        json.dump(fixture_json, fixture_stream)

    call_command('loaddata', fixture_file)

    musician = Musician.objects.get(id=expected_musician.id)

    assert musician.id == expected_musician.id
    assert musician.first_name == expected_musician.first_name
    assert musician.last_name == expected_musician.last_name
    assert musician.instrument == expected_musician.instrument


def test_complex_fixture(tmp_path):
    fixture_file = tmp_path / "fixture.json"

    expected_musician = MusicianFactory.build(id=1)
    expected_album = AlbumFactory.build(id=1, artist=expected_musician)

    # Sanity check
    assert not Musician.objects.filter(id=expected_musician.id).exists()
    assert not Album.objects.filter(id=expected_album.id).exists()

    fixture_json = [
        {
            'model': 'testapp.album',
            'fields': {
                'id': expected_album.id,
                'artist': expected_album.artist_id,
                'name': expected_album.name,
                'release_date': date_repr(expected_album.release_date)
            }
        },
        {
            'model': 'testapp.musician',
            'fields': {
                'id': expected_musician.id,
                'first_name': expected_musician.first_name,
                'last_name': expected_musician.last_name,
                'instrument': expected_musician.instrument
            }
        }
    ]


    with open(fixture_file, "w") as fixture_stream:
        json.dump(fixture_json, fixture_stream)

    call_command('loaddata', fixture_file)

    musician = Musician.objects.get(id=expected_musician.id)

    assert musician.id == expected_musician.id
    assert musician.first_name == expected_musician.first_name
    assert musician.last_name == expected_musician.last_name
    assert musician.instrument == expected_musician.instrument

    album = Album.objects.get(id=expected_album.id)

    assert album.artist == expected_musician
    assert album.name == expected_album.name
    assert album.release_date == expected_album.release_date


def test_corrupt_fixture_load(tmp_path):
    fixture_file = tmp_path / "fixture.json"

    assert not Musician.objects.exists()

    fixture_json = [
        {
            'model': 'testapp.musician',
        }
    ]

    with open(fixture_file, "w") as fixture_stream:
        json.dump(fixture_json, fixture_stream)

    with pytest.raises(DeserializationError) as exc_info:
        call_command('loaddata', fixture_file)

    assert exc_info.value.args[0] == f"Problem installing fixture '{fixture_file}': "
    assert not Musician.objects.exists()
