import django_filters

from recipes.models import Ingredient


class IngredientFilter(django_filters.FilterSet):
    class Meta:
        model = Ingredient
        fields = {
            'name': ['startswith'],
        }
