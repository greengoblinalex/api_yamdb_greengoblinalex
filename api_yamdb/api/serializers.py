from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.fields import DateTimeField, CharField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=serializers.CurrentUserDefault())
    pub_date = DateTimeField(read_only=True)

    class Meta:
        model = Review
        exclude = ('title',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=serializers.CurrentUserDefault())
    pub_date = DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
