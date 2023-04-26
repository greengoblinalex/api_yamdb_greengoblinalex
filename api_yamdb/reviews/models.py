from django.db import models

from .validators import validate_alphanumeric


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
    genres = models.ManyToManyField(Genre, through='TitleGenre')
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='titles',
    )
    description = models.TextField(default='', null=True, blank=True)
    rating = models.IntegerField(default=0)

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
