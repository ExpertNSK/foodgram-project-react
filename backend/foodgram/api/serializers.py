from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator
from djoser.serializers import TokenCreateSerializer

from users.models import User


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
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150, write_only=True)

    def validate_username(self, value):
        invalid_username = False
        fail_sym = r'^[\w.@+-]+\z'
        if value.lower() == 'me':
            invalid_username = True
        for chr in value:
            if chr in fail_sym:
                invalid_username = True
        if invalid_username:
            raise serializers.ValidationError(
                'Имя пользователя содержит недопустимые символы или равно "me"!',
            )
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