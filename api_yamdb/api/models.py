from django.db import models


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
