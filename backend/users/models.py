from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


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
        symmetrical=False,
        null=True,
        blank=True,
        related_name='subscribers',
        verbose_name='Любимые авторы',
    )
    username = models.CharField(
        max_length=150,
        validators=[validate_username],
        verbose_name='Логин',
    )
    favorite_recipes = models.ManyToManyField(
        'recipes.Recipe',
        null=True,
        blank=True,
        related_name='connoisseurs',
        verbose_name='Любимые рецепты',
    )
    shopping_list = models.ManyToManyField(
        'recipes.Recipe',
        null=True,
        blank=True,
        related_name='buyers',
        verbose_name='Покупки',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
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

    @property
    def is_admin(self):
        return self.role == 'admin'
