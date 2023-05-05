import re
from datetime import date

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import DateTimeField
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment, Review, Title, Genre, Category
from users.constants import USERNAME_PATTERN

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
                'Username should contain only letters,\
                 digits, and @/./+/-/_ characters.'
            )

        return data

    def validate_email(self, data):
        if len(data) > 254:
            raise serializers.ValidationError('Too long email')
        return data


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        user = User.objects.filter(email=data.get('email')).first()
        if user and user.username != data.get('username'):
            raise serializers.ValidationError(
                'Another user with this email already exists')

        user = User.objects.filter(username=data.get('username')).first()
        if user and user.username == data.get(
                'username') and user.email != data.get('email'):
            raise serializers.ValidationError('Wrong email already exists')
        return data

    def validate_username(self, data):
        if not re.match(USERNAME_PATTERN, data):
            raise serializers.ValidationError(
                'Username should contain only letters,\
                 digits, and @/./+/-/_ characters.'
            )
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
            raise serializers.ValidationError('Too long first name')
        return data

    def validate_last_name(self, data):
        if len(data) > 150:
            raise serializers.ValidationError('Too long last name')
        return data


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code', 'email')

    def validate(self, data):
        username = data.get('username')
        user = get_object_or_404(
            User,
            username=username,
        )
        data['user'] = user
        return data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'genre',
                  'description', 'category')

    def get_rating(self, obj):
        all_scores = obj.reviews.values_list('score', flat=True)

        if not all_scores:
            return None
        return int(sum(all_scores) / len(all_scores))


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         many=True)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'genre', 'description', 'category')

    def validate_year(self, value):
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                "Год выпуска не может быть больше текущего года"
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=serializers.CurrentUserDefault())
    pub_date = DateTimeField(read_only=True)
    title = serializers.IntegerField(write_only=True, default=None)

    class Meta:
        model = Review
        fields = ('id', 'author', 'pub_date', 'score', 'text', 'title')

    def validate_score(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError(
                'Score must be between 0 and 10')
        return value

    def save(self, **kwargs):
        if self.context['request'].method == 'POST' and \
                Review.objects.filter(author=kwargs['author'],
                                      title=kwargs['title']).exists():
            raise ValidationError(
                'Вы уже оставляли отзыв на это произведение')
        super().save(**kwargs)


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=serializers.CurrentUserDefault())
    pub_date = DateTimeField(read_only=True)
    review = serializers.IntegerField(write_only=True, default=None)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review')
