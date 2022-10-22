from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import FavoriteView, IngredientViewSet, RecipeViewSet, SubscriptionsView, TagViewSet, UserViewSet, ShoppingCartView


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('recipes/<int:id>/favorite/', FavoriteView.as_view()),
    path('recipes/<int:id>/shopping_cart/', ShoppingCartView.as_view()),
    path('users/<int:id>/subscribe/', SubscriptionsView.as_view())
]
