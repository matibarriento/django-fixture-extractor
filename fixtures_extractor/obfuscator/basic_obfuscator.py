from random import SystemRandom
from string import ascii_letters, digits

from django.db.models import EmailField

# TODO move these constants to settings
EMAIL_NAME_NAME_MAX_LENGTH = 10
EMAIL_DOMAIN_NAME_MAX_LENGTH = 10
EMAIL_DOMAIN_SUFFIX = "com"
PASSWORD_MAX_LENGTH = 10


class BasicObfuscator:
    def obfuscate(self, field, value):
        if isinstance(field, EmailField):
            obfuscated_email_name = "".join(
                SystemRandom().choice(ascii_letters + digits)
                for _ in range(EMAIL_NAME_NAME_MAX_LENGTH)
            )
            obfuscated_email_domain = "".join(
                SystemRandom().choice(ascii_letters + digits)
                for _ in range(EMAIL_DOMAIN_NAME_MAX_LENGTH)
            )
            return f"{obfuscated_email_name}@{obfuscated_email_domain}.{EMAIL_DOMAIN_SUFFIX}"

        if self._is_password_field(field):
            return "".join(
                SystemRandom().choice(ascii_letters + digits)
                for _ in range(PASSWORD_MAX_LENGTH)
            )

        return value

    def _is_password_field(self, field):
        # if getattr(field, "field_name", None) is None:
        #     return False
        return field.field_name == "password"
