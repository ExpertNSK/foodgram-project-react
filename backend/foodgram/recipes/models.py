from email.policy import default
from django.db import models
from django.core.validators import MinValueValidator

from .validators import SlugValidator
from users.models import User


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
    
    def __str__(self):
        return self.name


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
    
    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Теги',
        related_name='recipes',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
        related_name='recipes',
    )
    name = models.CharField(
        'Название',
        max_length=200,
    )
    image = models.ImageField(
        upload_to='images/',
        verbose_name='Изображение',
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1, 'Время приготовления не может быть меньше минуты!'
            )
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
    
    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name = 'Тег'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'tag'),
                name = 'recipe tag unique'
            )
        ]
        verbose_name='Тег в рецепте'
        verbose_name_plural='Теги в рецептах'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='recipe ingredient unique'
            )
        ]
