from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import DateTimeField
from rest_framework.relations import SlugRelatedField

from reviews.models import (Comment, Review, Title, Genre, Category, )


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
