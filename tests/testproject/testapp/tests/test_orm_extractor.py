import pytest

from fixtures_extractor.dtos import ModelFieldMetaDTO
from fixtures_extractor.enums import FieldType
from fixtures_extractor.orm_extractor import ORMExtractor


@pytest.mark.parametrize(
    "app_name, expected_fields",
    [
        (
            "testapp.Artist",
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
                    field_name="artist",
                    model_name="album",
                    field_type=FieldType.reverse_foreign_key,
                    is_model_declared=False,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="artists",
                    model_name="song",
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
                    field_name="id",
                    model_name="album",
                    field_type=FieldType.field,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="artist",
                    model_name="artist",
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
                    field_name="album",
                    model_name="song",
                    field_type=FieldType.reverse_foreign_key,
                    is_model_declared=False,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="record_label",
                    model_name="recordlabel",
                    field_type=FieldType.foreign_key,
                ),
            ],
        ),
        (
            "testapp.Song",
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
                    model_name="album",
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
                    model_name="artist",
                    field_type=FieldType.many_to_many,
                ),
            ],
        ),
    ],
)
def test_get_all_fields(app_name, expected_fields):
    orm_extractor = ORMExtractor()

    fields_names = orm_extractor.get_all_fields(app_model=app_name)

    assert sorted(fields_names) == sorted(expected_fields)


@pytest.mark.parametrize(
    "app_name, expected_model_fields",
    [
        (
            "testapp.Artist",
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
            "testapp.Album",
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
            "testapp.Song",
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
def test_get_model_fields(app_name, expected_model_fields):
    orm_extractor = ORMExtractor()

    fields_names = orm_extractor.get_model_fields(app_model=app_name)

    assert sorted(fields_names) == sorted(expected_model_fields)


@pytest.mark.parametrize(
    "app_model, expected_model_target_relations",
    [
        (
            "testapp.Artist",
            [
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="artist",
                    model_name="album",
                    field_type=FieldType.reverse_foreign_key,
                    is_model_declared=False,
                ),
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="artists",
                    model_name="song",
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
                    field_name="album",
                    model_name="song",
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

    model_target_relations = orm_extractor.get_model_target_relations(
        app_model=app_model
    )

    assert sorted(model_target_relations) == sorted(expected_model_target_relations)


@pytest.mark.parametrize(
    "app_model, expected_model_declared_many_relations",
    [
        (
            "testapp.Artist",
            [],
        ),
        (
            "testapp.Album",
            [],
        ),
        (
            "testapp.Song",
            [
                ModelFieldMetaDTO(
                    app_name="testapp",
                    field_name="artists",
                    model_name="artist",
                    field_type=FieldType.many_to_many,
                ),
            ],
        ),
    ],
)
def test_get_model_declared_many_relations(
    app_model, expected_model_declared_many_relations
):
    orm_extractor = ORMExtractor()

    model_target_relations = orm_extractor.get_model_declared_many_relations(
        app_model=app_model
    )

    assert sorted(model_target_relations) == sorted(
        expected_model_declared_many_relations
    )
