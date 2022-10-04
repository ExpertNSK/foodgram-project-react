from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import password_validation
from django.core.validators import MinValueValidator
from drf_extra_fields.fields import Base64ImageField

from users.models import User
from users.validators import validate_username
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag


class PasswordEditSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(
        max_length=150,
        required=True,
        write_only=True
    )
    current_password = serializers.CharField(
        max_length=150,
        required=True,
        write_only=True
    )

    def validate_new_password(self, value):
        if value is None or value == '':
            return serializers.ValidationError(
                {"new_password": "Обязательное поле."}
            )
        password_validation.validate_password(value, self.instance)
        return value
    
    def validate_current_password(self, value):
        if value is None or value == '':
            return serializers.ValidationError(
                {"current_password": "Обязательное поле."}
            )
        return value

    class Meta:
        model = User
        fields = ('current_password', 'new_password',)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            validate_username,
        ]
    )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150, write_only=True)
    
    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'password',
        )

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit',
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'color', 'slug',
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = (
            'id', 'name', 'measurement_unit', 'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time',
        )
    
    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(ingredients, many=True).data
