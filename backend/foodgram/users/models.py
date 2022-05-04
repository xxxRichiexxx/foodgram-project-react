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

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    """Модель подписок."""
    subscriber_id = models.ForeignKey(
        CustomUser,
        related_name="subscriptions",
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        )
    author_id = models.ForeignKey(
        CustomUser,
        related_name="subscribers",
        on_delete=models.CASCADE,
        verbose_name='Автор',
        )
    date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата',
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber_id','author_id'],
                name="unique_followers"
                )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.subscriber_id.username} -- {self.author_id.username}'