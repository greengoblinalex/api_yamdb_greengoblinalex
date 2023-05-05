import re
from datetime import date

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.fields import DateTimeField

from reviews.models import Comment, Review, Title, Genre, Category, TitleGenre
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
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField('title_rating')

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'genre',
                  'description', 'category')

    def title_rating(self, obj):
        all_scores = obj.reviews.values_list('score', flat=True)

        if not all_scores:
            return None

        return int(sum(all_scores) / len(all_scores))

    def validate_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Год выпуска не может быть "
                                              "больше текущего года")
        return value

    def get_genre(self, obj):
        return GenreSerializer(obj.genre, many=True).data

    def get_category(self, obj):
        return CategorySerializer(obj.category).data

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        category = validated_data.pop('category')
        category = Category.objects.get(slug=category)

        title = Title.objects.create(**validated_data, category=category)
        for genre in genres:
            genre = Genre.objects.get(slug=genre)
            TitleGenre.objects.create(title=title, genre=genre)
        return title

    def update(self, title, validated_data):
        genres = validated_data.pop('genre')
        category = validated_data.pop('category')
        category = Category.objects.get(slug=category)

        if category:
            setattr(title, 'category', category)
        for (key, value) in validated_data.items():
            setattr(title, key, value)
        title.save()

        if genres:
            for genre in genres:
                genre = Genre.objects.get(slug=genre)
                TitleGenre.objects.create(title=title, genre=genre)
        return title


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
