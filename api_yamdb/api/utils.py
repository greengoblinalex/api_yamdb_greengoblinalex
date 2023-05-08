import re

from rest_framework import serializers

USERNAME_PATTERN = r'^[\w.@+-]+$'


def validate_username(username):
    if not re.match(USERNAME_PATTERN, username):
        raise serializers.ValidationError(
            'Username should contain only '
            'letters, digits, and @/./+/-/_ characters.'
        )
    return username
