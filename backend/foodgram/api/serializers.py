from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator
from django.contrib.auth import password_validation

from users.models import User


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