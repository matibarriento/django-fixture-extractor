from enum import Enum


class FieldType(Enum):
    field = "field"
    many_to_many = "many_to_many"
    foreign_key = "foreign_key"
    reverse_foreign_key = "reverse_foreign_key"
    one_to_one = "one_to_one"
