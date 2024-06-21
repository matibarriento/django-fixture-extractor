import pytest

from fixtures_extractor.enums import FieldType
from fixtures_extractor.orm_extractor import ModelFieldMetaDTO, ORMExtractor
from tests.testproject.testapp.factories import ArtistFactory, AlbumFactory, SongFactory
from tests.testproject.testapp.models import Album, Artist, Song

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    "app_model, model_factory, filter_key",
    [
        ("testapp.Artist", ArtistFactory, "id"),
        ("testapp.Album", AlbumFactory, "id"),
        ("testapp.Song", SongFactory, "id"),
    ],
)
def test_get_records(
    app_model,
    model_factory,
    filter_key,
):
    check_instance = model_factory.create()
    model_factory.create()

    orm_extractor = ORMExtractor()

    records = orm_extractor.get_records(
        app_model=app_model,
        filter_key=filter_key,
        filter_value=getattr(check_instance, filter_key),
    )

    fields = orm_extractor.get_model_fields(app_model=app_model)
    field_names = [field.field_name for field in fields]

    assert len(records) == 1
    assert records[0] == {
        field_name: getattr(check_instance, field_name) for field_name in field_names
    }


@pytest.mark.parametrize(
    "app_model, model_factory",
    [
        ("testapp.Artist", ArtistFactory),
        ("testapp.Album", AlbumFactory),
        ("testapp.Song", SongFactory),
    ],
)
def test_build_records(
    app_model,
    model_factory,
):
    orm_extractor = ORMExtractor()

    fields = orm_extractor.get_model_fields(app_model=app_model)
    field_names = [field.field_name for field in fields]

    factory_records = [
        model_factory.create(),
        model_factory.create(),
        model_factory.create(),
    ]

    records = [
        {field_name: getattr(instance, field_name) for field_name in field_names}
        for instance in factory_records
    ]

    built_records = orm_extractor.build_records(app_model=app_model, records=records)

    assert built_records == [
        {
            "model": app_model,
            "fields": record,
        }
        for record in records
    ]


@pytest.mark.parametrize(
    "app_model, expected_model",
    [
        ("testapp.Artist", Artist),
        ("testapp.Album", Album),
        ("testapp.Song", Song),
    ],
)
def test_get_model(app_model, expected_model):
    orm_extractor = ORMExtractor()

    model = orm_extractor.get_model(app_model=app_model)

    assert model == expected_model


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
    "app_model, expected_model_fields",
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
def test_get_model_fields(app_model, expected_model_fields):
    orm_extractor = ORMExtractor()

    fields_names = orm_extractor.get_model_fields(app_model=app_model)

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
