import pytest

from fixtures_extractor.enums import FieldType
from fixtures_extractor.orm_extractor import ModelFieldMetaDTO, ORMExtractor
from tests.testproject.testapp.models import Album, Artist, Song


@pytest.mark.parametrize(
    "Model, expected_fields",
    [
        (
            Artist,
            [
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="id",
                    model_name="artist",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="first_name",
                    model_name="artist",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="last_name",
                    model_name="artist",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="instrument",
                    model_name="artist",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="albums",
                    model_name="artist",
                    field_type=FieldType.reverse_foreign_key,
                    is_model_declared=False,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="songs",
                    model_name="artist",
                    field_type=FieldType.many_to_many,
                    is_model_declared=False,
                ),
            ],
        ),
        (
            Album,
            [
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="id",
                    model_name="album",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="artist",
                    model_name="album",
                    field_type=FieldType.foreign_key,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="name",
                    model_name="album",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="release_date",
                    model_name="album",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="songs",
                    model_name="album",
                    field_type=FieldType.reverse_foreign_key,
                    is_model_declared=False,
                ),
            ],
        ),
        (
            Song,
            [
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="id",
                    model_name="song",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="album",
                    model_name="song",
                    field_type=FieldType.foreign_key,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="name",
                    model_name="song",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="release_date",
                    model_name="song",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="artists",
                    model_name="song",
                    field_type=FieldType.many_to_many,
                ),
            ],
        ),
    ],
)
def test_get_all_fields(Model, expected_fields):
    orm_extractor = ORMExtractor()

    fields_names = orm_extractor.get_all_fields(Model=Model)

    assert sorted(fields_names) == sorted(expected_fields)


@pytest.mark.parametrize(
    "Model, expected_model_fields",
    [
        (
            Artist,
            [
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="id",
                    model_name="artist",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="first_name",
                    model_name="artist",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="last_name",
                    model_name="artist",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="instrument",
                    model_name="artist",
                    field_type=FieldType.field,
                ),
            ],
        ),
        (
            Album,
            [
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="id",
                    model_name="album",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="name",
                    model_name="album",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="release_date",
                    model_name="album",
                    field_type=FieldType.field,
                ),
            ],
        ),
        (
            Song,
            [
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="id",
                    model_name="song",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="name",
                    model_name="song",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="release_date",
                    model_name="song",
                    field_type=FieldType.field,
                ),
            ],
        ),
    ],
)
def test_get_model_fields(Model, expected_model_fields):
    orm_extractor = ORMExtractor()

    fields_names = orm_extractor.get_model_fields(Model=Model)

    assert sorted(fields_names) == sorted(expected_model_fields)


@pytest.mark.parametrize(
    "Model, expected_m2m_fields",
    [
        (
            Artist,
            [
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="songs",
                    model_name="artist",
                    field_type=FieldType.many_to_many,
                    is_model_declared=False,
                )
            ],
        ),
        (Album, []),
        (
            Song,
            [
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="artists",
                    model_name="song",
                    field_type=FieldType.many_to_many,
                )
            ],
        ),
    ],
)
def test_get_many_to_many_relations(Model, expected_m2m_fields):
    orm_extractor = ORMExtractor()

    m2m_fields_names = orm_extractor.get_many_to_many_relations(Model=Model)

    assert sorted(m2m_fields_names) == sorted(expected_m2m_fields)


@pytest.mark.parametrize(
    "Model, expected_relation_fields",
    [
        (
            Artist,
            [
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="albums",
                    model_name="artist",
                    field_type=FieldType.reverse_foreign_key,
                    is_model_declared=False,
                ),
            ],
        ),
        (
            Album,
            [
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="songs",
                    model_name="album",
                    field_type=FieldType.reverse_foreign_key,
                    is_model_declared=False,
                )
            ],
        ),
        (Song, []),
    ],
)
def test_get_reverse_relations(Model, expected_relation_fields):
    orm_extractor = ORMExtractor()

    reverse_relations = orm_extractor.get_reverse_relations(Model=Model)

    assert sorted(reverse_relations) == sorted(expected_relation_fields)


@pytest.mark.parametrize(
    "app_model, expected_model_declared_relations",
    [
        (
            "testapp.Artist",
            [],
        ),
        (
            "testapp.Album",
            [
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="artist",
                    model_name="album",
                    field_type=FieldType.foreign_key,
                    is_model_declared=True,
                ),
            ],
        ),
        (
            "testapp.Song",
            [
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="artists",
                    model_name="song",
                    field_type=FieldType.many_to_many,
                    is_model_declared=True,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="album",
                    model_name="song",
                    field_type=FieldType.foreign_key,
                    is_model_declared=True,
                ),
            ],
        ),
    ],
)
def test_get_model_declared_relations(app_model, expected_model_declared_relations):
    orm_extractor = ORMExtractor()

    model_declared_relations = orm_extractor.get_model_declared_relations(app_model)

    assert sorted(model_declared_relations) == sorted(expected_model_declared_relations)


@pytest.mark.parametrize(
    "app_model, expected_model_target_relations",
    [
        (
            "testapp.Artist",
            [
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="albums",
                    model_name="artist",
                    field_type=FieldType.reverse_foreign_key,
                    is_model_declared=False,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="songs",
                    model_name="artist",
                    field_type=FieldType.many_to_many,
                    is_model_declared=False,
                ),
            ],
        ),
        (
            "testapp.Album",
            [
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="songs",
                    model_name="album",
                    field_type=FieldType.reverse_foreign_key,
                    is_model_declared=False,
                ),
            ],
        ),
        (
            "testapp.Song",
            [],
        ),
    ],
)
def test_get_model_target_relations(app_model, expected_model_target_relations):
    orm_extractor = ORMExtractor()

    model_target_relations = orm_extractor.get_model_target_relations(app_model)

    assert sorted(model_target_relations) == sorted(expected_model_target_relations)
