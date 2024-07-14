import pytest
from django.db.models import (
    EmailField,
    CharField,
)

from fixtures_extractor.obfuscator.basic_obfuscator import BasicObfuscator


@pytest.mark.parametrize(
    "field, expected_obfuscated_value",
    [
        (CharField(), "sample_char_field"),
    ],
)
def test_not_supported_obfuscation(field, expected_obfuscated_value):
    # Revisit when Descriptors tests are implemented
    obfuscator = BasicObfuscator()
    obfuscated_value = obfuscator.obfuscate(field, expected_obfuscated_value)

    assert obfuscated_value == expected_obfuscated_value


def test_email_field_obfuscation():
    email = "sample_email@tests.com"
    email_field = EmailField()
    # email_field.field_name = email

    obfuscator = BasicObfuscator()
    obfuscated_email = obfuscator.obfuscate(email_field, email)

    assert email != obfuscated_email
    assert "@" in obfuscated_email
    assert "." in obfuscated_email
