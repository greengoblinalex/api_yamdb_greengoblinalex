from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import authenticate

from .models import User


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=False)

    class Meta:
        fields = '__all__'
        model = User

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)

    class Meta:
        fields = '__all__'
        model = User

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        confirmation_code = data.get('confirmation_code')

        if username and password:
            user = authenticate(
                username=username,
                password=password,
            )

            if not user:
                raise serializers.ValidationError(
                    'Incorrect username or password')
            elif user.confirmation_code != confirmation_code:
                raise serializers.ValidationError(
                    'Incorrect confirmation code')

            data['user'] = user
            return data
