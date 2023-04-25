from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.fields import DateTimeField

from reviews.models import Comment, Review


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
            raise serializers.ValidationError('Score must be between 0 and 10')
        return value

    def save(self, **kwargs):
        if self.context['request'].method == 'POST' and \
                Review.objects.filter(author=kwargs['author'],
                                      title=kwargs['title']).exists():
            raise ValidationError('Вы уже оставляли отзыв на это произведение')
        super().save(**kwargs)


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=serializers.CurrentUserDefault())
    pub_date = DateTimeField(read_only=True)
    review = serializers.IntegerField(write_only=True, default=None)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review')
