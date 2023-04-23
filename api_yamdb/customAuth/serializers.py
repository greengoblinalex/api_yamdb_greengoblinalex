import re

from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import User
from users.constants import USERNAME_PATTERN


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        fields = ('email', 'username')
        model = User

    def validate(self, data):
        user = User.objects.filter(email=data.get('email')).first()
        if user and user.username != data.get('username'):
            raise serializers.ValidationError(
                'Another user with this email already exists')

        user = User.objects.filter(username=data.get('username')).first()
        if user and user.username == data.get('username') and user.email != data.get('email'):
            raise serializers.ValidationError('Wrong email already exists')
        return data

    def validate_username(self, data):
        if not re.match(USERNAME_PATTERN, data):
            raise serializers.ValidationError(
                'Username should contain only letters, digits, and @/./+/-/_ characters.')
        elif data == 'me':
            raise serializers.ValidationError(
                'Invalid username: "me" is a reserved keyword')
        elif len(data) > 150:
            raise serializers.ValidationError('Too long username')
        return data

    def validate_email(self, data):
        if len(data) > 254:
            raise serializers.ValidationError('Too long email')
        return data

    def validate_first_name(self, data):
        if len(data) > 150:
            raise serializers.ValidationError('Too first name')
        return data

    def validate_last_name(self, data):
        if len(data) > 150:
            raise serializers.ValidationError('Too last name')
        return data


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=False)

    class Meta:
        fields = ('username', 'confirmation_code', 'email')
        model = User

    def validate(self, data):
        username = data.get('username')
        user = get_object_or_404(
            User,
            username=username,
        )
        data['user'] = user
        return data
