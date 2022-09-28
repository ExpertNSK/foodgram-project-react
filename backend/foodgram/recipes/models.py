from django.db import models
from django.contrib.postgres.indexes import GinIndex

from .validators import SlugValidator


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        unique=True,
        blank=False,
    )
    color = models.CharField(
        'Цвет в HEX',
        max_length=7,
        blank=False,
        unique=True,
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=200,
        unique=True,
        blank=False,
        validators=[SlugValidator,]
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        db_index=True,
        max_length=200,
        blank = False,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
        blank = False,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингридиенты'
        unique_together = ('name', 'measurement_unit',)

