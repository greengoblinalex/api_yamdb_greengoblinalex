import re

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .constants import USERNAME_PATTERN

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, data):
        if not re.match(USERNAME_PATTERN, data):
            raise serializers.ValidationError(
                'Username should contain only letters, digits, and @/./+/-/_ characters.')
        return data

    def validate_email(self, data):
        if len(data) > 254:
            raise serializers.ValidationError('Too long email')
        return data
