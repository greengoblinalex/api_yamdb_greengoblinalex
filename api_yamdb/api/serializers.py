from datetime import date

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import DateTimeField
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Review, Title, Genre, Category, TitleGenre


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

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]

    def validate_score(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError(
                'Score must be between 0 and 10')
        return value

    def validate(self, data):
        if (self.context['request'].method == 'POST'
                and Review.objects.filter(
                    author=self.context['author'], title=self.context['title']
                ).exists()):
            raise ValidationError('Вы уже оставляли отзыв на это произведение')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=serializers.CurrentUserDefault())
    pub_date = DateTimeField(read_only=True)
    review = serializers.IntegerField(write_only=True, default=None)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review')
