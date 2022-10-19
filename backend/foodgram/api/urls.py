from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import FavoriteViewSet, IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('recipes/<int:id>/favorite/', FavoriteViewSet.as_view())
]
