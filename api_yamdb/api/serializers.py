from rest_framework import serializers
from datetime import date

from reviews.models import Title, Genre, Category, TitleGenre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def validate_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Год выпуска не может быть "
                                              "больше текущего года")
        return value

    def get_category(self, obj):
        return {
            'name': obj.category.name,
            'slug': obj.category.slug,
        }

    def create(self, validated_data):
        print(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TitleGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleGenre
        fields = ('id')
