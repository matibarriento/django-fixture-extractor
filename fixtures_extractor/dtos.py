from dataclasses import dataclass

from django.db.models.fields.related import ForeignObjectRel

from fixtures_extractor.enums import FieldType


@dataclass
class ModelFieldMetaDTO:
    app_name: str
    field_name: str
    model_name: str
    field_type: FieldType
    is_model_declared: bool = True

    @staticmethod
    def build(field):
        app_name = field.model._meta.app_label
        model_name = field.model._meta.model_name
        field_name = field.name
        field_type = ModelFieldMetaDTO._detect_field_type(field=field)
        is_model_declared = ModelFieldMetaDTO._detect_model_declaration(field=field)

        if is_model_declared and field_type != FieldType.field:
            app_name = field.related_model._meta.app_label
            model_name = field.related_model._meta.model_name

        if field.is_relation and not is_model_declared:
            app_name = field.related_model._meta.app_label
            model_name = field.related_model._meta.model_name
            field_name = field.field.name

        return ModelFieldMetaDTO(
            app_name=app_name,
            field_name=field_name,
            model_name=model_name,
            field_type=field_type,
            is_model_declared=is_model_declared,
        )

    @classmethod
    def _detect_field_type(cls, field) -> FieldType:
        if not field.is_relation:
            return FieldType.field

        if field.many_to_many:
            return FieldType.many_to_many

        if field.one_to_one:
            return FieldType.one_to_one

        if field.many_to_one:
            return FieldType.foreign_key

        if field.one_to_many:
            return FieldType.reverse_foreign_key

        raise ValueError(f"Unknown field type: {field}")

    @classmethod
    def _detect_model_declaration(cls, field) -> bool:
        return not isinstance(field, ForeignObjectRel)

    def __eq__(self, value: object) -> bool:
        if self.app_name != value.app_name:
            return False

        if self.field_name != value.field_name:
            return False

        if self.model_name != value.model_name:
            return False

        if self.field_type != value.field_type:
            return False

        if self.is_model_declared != value.is_model_declared:
            return False

        return True

    def __gt__(self, value: object) -> bool:
        return self.field_name > value.field_name

    def __lt__(self, value: object) -> bool:
        return self.field_name < value.field_name
