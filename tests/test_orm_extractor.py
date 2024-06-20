import pytest

from fixtures_extractor.orm_extractor import ORMExtractor
from tests.testproject.testapp.models import Artist, Album, Song


@pytest.mark.parametrize(
    "Model, expected_fields",
    [
        (Artist, ["id", "first_name", "last_name", "instrument"]),
        (Album, ["id", "artist", "name", "release_date"]),
        (Song, ["id", "album", "name", "release_date"]),
    ],
)
def test_discover_fields(Model, expected_fields):
    orm_extractor = ORMExtractor()

    fields_names = orm_extractor.get_fields(Model=Model)

    assert fields_names == expected_fields


@pytest.mark.parametrize(
    "Model, expected_m2m_fields",
    [
        (Artist, []),
        (Album, []),
        (Song, ["artists"]),
    ],
)
def test_discover_m2m_fields(Model, expected_m2m_fields):
    orm_extractor = ORMExtractor()

    m2m_fields_names = orm_extractor.get_many_to_many_relations(Model=Model)

    assert m2m_fields_names == expected_m2m_fields


@pytest.mark.parametrize(
    "Model, expected_relation_fields",
    [
        (Artist, ["albums", "songs"]),
        (Album, ["songs"]),
        (Song, []),
    ],
)
def test_get_revere_relations(Model, expected_relation_fields):
    orm_extractor = ORMExtractor()

    reverse_relations = orm_extractor.get_reverse_relations(Model=Model)

    assert reverse_relations == expected_relation_fields


@pytest.mark.parametrize(
    "Model, expected_attributes",
    [
        (Artist, ["id", "first_name", "last_name", "instrument", "albums", "songs"]),
        (Album, ["id", "artist", "name", "release_date", "songs"]),
        (Song, ["id", "album", "name", "release_date", "artists"]),
    ],
)
def test_get_all_model_attributes(Model, expected_attributes):
    orm_extractor = ORMExtractor()

    all_attributes = orm_extractor.get_all_model_attributes(Model=Model)

    assert all_attributes == expected_attributes
