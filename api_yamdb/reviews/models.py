from django.contrib.auth import get_user_model
from django.db import models

from .validators import validate_alphanumeric, score_validator

User = get_user_model()


class Genre(models.Model):
    name = models.TextField(max_length=256, )
    slug = models.SlugField(
        max_length=50, validators=(validate_alphanumeric,),
        unique=True
    )

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.TextField(max_length=256)
    year = models.IntegerField()
    genre = models.ManyToManyField(Genre, through='TitleGenre')
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='titles',
    )
    description = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.TextField(max_length=256, )
    slug = models.SlugField(
        max_length=50, validators=(validate_alphanumeric,),
        unique=True
    )

    def __str__(self):
        return self.slug


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title_genres'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='title_genres'
    )

    def __str__(self):
        return f'{self.title} - {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(Title, related_name='reviews',
                              on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='reviews',
                               on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField(validators=(score_validator,))
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
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

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']
