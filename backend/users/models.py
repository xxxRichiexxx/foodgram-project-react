from django.db import models
from django.contrib.auth.models import AbstractUser
from django.apps import apps

# from main.models import Recipe
# Recipe = apps.get_model(app_label='main', model_name='Recipe')

class CustomUser(AbstractUser):
    """Модель пользователя."""
    ROLES = (
        ('guest', 'Гость'),
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        verbose_name='Роль',
    )
    authors = models.ManyToManyField(
        'self',
        symmetrical = False,
        null=True,
        blank=True,
        related_name = 'subscribers',
        verbose_name='Любимые авторы',
    )
    favorite_recipes = models.ManyToManyField(
        'main.Recipe',
        null=True,
        blank=True,
        related_name = 'connoisseurs',
        verbose_name='Любимые рецепты',       
    )
    first_name = models.CharField(
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'