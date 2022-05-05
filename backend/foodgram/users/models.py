from django.db import models
from django.contrib.auth.models import AbstractUser


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
    )

    class Meta:
        default_related_name = 'subscribers'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'