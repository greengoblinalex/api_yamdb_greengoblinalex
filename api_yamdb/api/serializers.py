from datetime import date

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.fields import DateTimeField

from reviews.models import Comment, Review, Title, Genre, Category, TitleGenre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField('title_rating')

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'genres',
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

    def get_genres(self, obj):
        return GenreSerializer(obj.genres, many=True).data

    def get_category(self, obj):
        return CategorySerializer(obj.category).data

    def create(self, validated_data):
        genres = validated_data.pop('genres')
        category = validated_data.pop('category')
        category = Category.objects.get(slug=category)

        title = Title.objects.create(**validated_data, category=category)
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
