from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import UsernameValidator


USER = 'user'
ADMIN = 'admin'

ROLE_CHOICES = [
    (USER, 'user'),
    (ADMIN, 'admin')
]


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[UsernameValidator,]
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=False,
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        blank=False,
    )
    role = models.CharField(
        'Роль',
        max_length=max(len(role[1]) for role in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    @property
    def is_admin(self):
        return (
            self.role == ADMIN
            or self.is_superuser
            or self.is_staff
        )
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self) -> str:
        return self.username