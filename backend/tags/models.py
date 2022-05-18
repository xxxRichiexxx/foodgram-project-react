from django.db import models

from .validators import validate_color


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Название',
    )
    color = models.CharField(
        unique=True,
        max_length=7,
        validators=[validate_color],
        verbose_name='Цвет',
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        verbose_name='Идентификатор',
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name
