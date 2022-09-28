from django.db import models
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
