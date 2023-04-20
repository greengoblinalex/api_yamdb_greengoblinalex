from django.contrib.auth import get_user_model
from django.db import models

from .validators import score_validator

User = get_user_model()


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ForeignKey(
        'Genre', on_delete=models.CASCADE,
        related_name='titles', blank=True,
    )
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE,
        related_name='titles', blank=True,
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    ...


class Category(models.Model):
    ...



class Review(models.Model):
    title = models.ForeignKey(Title, related_name='reviews',
                              on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='reviews',
                               on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField(validators=(score_validator,))
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
    author = models.ForeignKey(User, related_name='comments',
                               on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
