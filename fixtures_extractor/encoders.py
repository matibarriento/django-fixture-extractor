from enum import Enum

from django.core.serializers.json import DjangoJSONEncoder


class EnhancedDjangoJSONEncoder(DjangoJSONEncoder):
    """Default DjangoJSONEncoder does not support Enum"""

    def default(self, o):
        if isinstance(o, Enum):
            # Currently support enum as value
            return o.value

        # Call super to continue with the default encoders
        return super().default(o)
