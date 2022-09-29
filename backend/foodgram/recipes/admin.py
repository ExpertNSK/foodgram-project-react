from django.contrib import admin
from .models import Recipe, RecipeIngredient, RecipeTag, Tag, Ingredient


class TagsInline(admin.TabularInline):
    model = RecipeTag
    extra = 1


class IngredientsInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug',)
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'pub_date',)
    inlines = (TagsInline, IngredientsInline,)
    search_fields = ('name', 'author__username', 'ingredients__name')
    list_filter = ('pub_date', 'tags')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
