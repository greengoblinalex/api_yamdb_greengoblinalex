from django.db import models

from api.models import Title
from .validators import score_validator


class Review(models.Model):
    title = models.ForeignKey(Title, related_name='reviews',
                              on_delete=models.CASCADE)
    author = models.ForeignKey('User', related_name='reviews',
                               on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField(validators=score_validator)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_title_author'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(Review, related_name='comments',
                               on_delete=models.CASCADE)
    author = models.ForeignKey('User', related_name='comments',
                               on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
