from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import UserViewSet


router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
