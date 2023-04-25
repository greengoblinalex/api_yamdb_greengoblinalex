from rest_framework import serializers
from datetime import date

from reviews.models import Title, Genre, Category, TitleGenre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'genre',
                  'description', 'category')

    def validate_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Год выпуска не может быть "
                                              "больше текущего года")
        return value

    def get_genre(self, obj):
        return GenreSerializer(obj.genre, many=True).data

    def get_category(self, obj):
        return {
            'name': obj.category.name,
            'slug': obj.category.slug,
        }

    def create(self, validated_data):
        print(validated_data)
        genres = validated_data.pop('genre')
        category = validated_data.pop('category')
        category = Category.objects.get(slug=category)

        title = Title.objects.create(**validated_data, category=category)
        for genre in genres:
            genre = Genre.objects.get(slug=genre)
            TitleGenre.objects.create(title=title, genre=genre)
        return title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TitleGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleGenre
        fields = ('id')
