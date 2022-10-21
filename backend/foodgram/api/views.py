from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, views
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.models import User, Subscription
from recipes.models import Ingredient, Recipe, Tag, Favorite
from .serializers import CreateRecipeSerializer, FavoriteSerializer, IngredientSerializer, PasswordEditSerializer, RecipeSerializer, ShowSubscribesSerializer, SubscribeSerializer, TagSerializer, UserSerializer, ShowFavoriteSerializer
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class SubscriptionsView(views.APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        data = {
            'user': user.id,
            'author': author.id
        }
        subscribe = Subscription.objects.filter(user=user, author=author).exists()
        if not subscribe:
            serializer = SubscribeSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if Subscription.objects.filter(user=user, author=author).exists():
            Subscription.objects.filter(user=user, author=author).delete()
            return Response(status.HTTP_204_NO_CONTENT)
        return Response(status.HTTP_400_BAD_REQUEST)


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly,]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return CreateRecipeSerializer
    
    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_favorite = self.request.query_params.get('is_favorite')
        author = self.request.query_params.get('author')
        tags = self.request.query_params.get('tags')
        if is_favorite == '1':
            queryset = queryset.filter(favorites__user=self.request.user)
        if author is not None:
            queryset = queryset.filter(author__id=author)
        if tags is not None:
            queryset = queryset.filter(tags__slug=tags)
        return queryset
    

class FavoriteView(views.APIView):
    @permission_classes(IsAuthenticated)
    def post(self, request, id):
        user = request.user.id
        recipe = get_object_or_404(Recipe, id=id)
        data = {
            'user': user,
            'recipe': recipe.id
        }
        if not Favorite.objects.filter(
            user=user, recipe=recipe).exists():
            serializer = FavoriteSerializer(
                data=data, context={'request': request}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)
    
    @permission_classes(IsAuthenticated)
    def delete(self, request, id):
        recipe =get_object_or_404(Recipe, id=id)
        if Favorite.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            Favorite.objects.filter(user=request.user, recipe=recipe).delete()
            return Response(status.HTTP_204_NO_CONTENT)
        return Response(status.HTTP_400_BAD_REQUEST)


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__contains=name)
        return queryset


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

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
    
    @action(
        ['GET'],
        detail=False,
        url_path='subscriptions',
        serializer_class=ShowSubscribesSerializer,
        permission_classes=[IsAuthenticated,]
    )
    def subscriptions(self, request):
        queryset = Subscription.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
