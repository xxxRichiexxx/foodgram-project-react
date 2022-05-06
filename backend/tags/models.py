from django.db import models


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        unique=True,
        max_length=50,
        verbose_name='Название',
    )
    color = models.CharField(
        unique=True,
        max_length=50,
        verbose_name='Цвет',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural ='Тэги'

    def __str__(self):
        return self.name
