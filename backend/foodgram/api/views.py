from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User
from recipes.models import Tag
from .serializers import PasswordEditSerializer, TagSerializer, UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        ['GET'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated,]
    )
    def user_profile(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status.HTTP_200_OK)
    
    @action(
        ['POST'],
        detail=False,
        url_path='set_password',
        serializer_class=PasswordEditSerializer,
        permission_classes=[IsAuthenticated,]
    )
    def change_password(self, request):
        user = request.user
        serializer = self.get_serializer(
            user,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        curr_psswd = request.data.get('current_password')
        if not user.check_password(curr_psswd):
            return Response(
                {"current_password": "Wrong password."},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(request.data.get('new_password'))
        user.save()
        return Response("Пароль успешно изменен.", status.HTTP_204_NO_CONTENT)
