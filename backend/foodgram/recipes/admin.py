from django.contrib import admin
from .models import Tag, Ingredient


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug',)
    search_fields = ('name',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
