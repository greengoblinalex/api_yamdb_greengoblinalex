from django.contrib.auth import get_user_model
from django.db import models

from .validators import validate_alphanumeric, score_validator

User = get_user_model()


class Genre(models.Model):
    name = models.TextField(max_length=256, verbose_name='slug')
    slug = models.SlugField(
        max_length=50, validators=(validate_alphanumeric,),
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.TextField(max_length=256, verbose_name='name')
    year = models.IntegerField(verbose_name='year')
    genre = models.ManyToManyField(Genre, verbose_name='genre')
    category = models.ForeignKey('Category', on_delete=models.CASCADE,
                                 related_name='titles', verbose_name='category')
    description = models.TextField(default='', null=True, blank=True,
                                   verbose_name='description')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.TextField(max_length=256, verbose_name='name')
    slug = models.SlugField(
        max_length=50, validators=(validate_alphanumeric,),
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


# class TitleGenre(models.Model):
#     title = models.ForeignKey(
#         Title,
#         on_delete=models.CASCADE,
#         related_name='title_genres'
#     )
#     genre = models.ForeignKey(
#         Genre,
#         on_delete=models.CASCADE,
#         related_name='title_genres'
#     )
#
#     def __str__(self):
#         return f'{self.title} - {self.genre}'


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
