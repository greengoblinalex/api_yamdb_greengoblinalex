from django.db import models

from .validators import validate_alphanumeric


class Title(models.Model):
    """Модель произведений искусства"""
    name = models.TextField(max_length=256,)
    year = models.IntegerField()
    rating = models.IntegerField()
    description = models.TextField()
    genre = models.ForeignKey(
        'Genre', on_delete=models.CASCADE, related_name='titles',
    )
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='titles',
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров искусства"""
    name = models.TextField(max_length=256, )
    slug = models.SlugField(
        max_length=50, validators=(validate_alphanumeric,),
        unique=True
    )


class Category(models.Model):
    """Модель категорий искусства"""
    name = models.TextField(max_length=256, )
    slug = models.SlugField(
        max_length=50, validators=(validate_alphanumeric,),
        unique=True
    )
