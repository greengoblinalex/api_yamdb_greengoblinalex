from datetime import date

from rest_framework import serializers
from reviews.models import Title, Genre, Category, TitleGenre


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

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'genres',
                  'description', 'category')

    def validate_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Год выпуска не может быть "
                                              "больше текущего года")
        return value

    def get_genre(self, obj):
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
