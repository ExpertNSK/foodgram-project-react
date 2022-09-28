from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import IngredientViewSet, TagViewSet, UserViewSet


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
