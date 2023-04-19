import re
from django.core.exceptions import ValidationError


def validate_alphanumeric(value):
    pattern = re.compile(r'^[a-zA-Z0-9]+$')
    if not pattern.match(value):
        raise ValidationError(
            'The value should contain only alphanumeric characters'
        )
