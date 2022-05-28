from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.contrib.contenttypes.models import ContentType

from .validators import validate_username
from ingredients.models import Ingredient


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

    def save(self, *args, **kwargs):
        self.is_staff = self.is_admin
        content_type = ContentType.objects.get_for_model(Ingredient)
        ingredient_permission = Permission.objects.filter(
            content_type=content_type
        )
        if self.is_staff:
            for perm in ingredient_permission:
                self.user_permissions.add(perm)
        else:
            for perm in ingredient_permission:
                self.user_permissions.remove(perm)
        super().save(*args, **kwargs)
