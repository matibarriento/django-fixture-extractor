import json

import pytest
from django.core.management import call_command
from django.core.serializers.base import DeserializationError

from tests.factories import MusicianFactory
from tests.testproject.testapp.models import Musician

pytestmark = [pytest.mark.django_db]


def test_fixture_load(tmp_path):
    fixture_file = tmp_path / "fixture.json"

    expected_musician = MusicianFactory()

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
