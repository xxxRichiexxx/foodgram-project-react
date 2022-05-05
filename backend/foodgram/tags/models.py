from django.db import models


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        max_length=50,
        verbose_name='Название',
    )
    color = models.CharField(
        max_length=50,
        verbose_name='Цвет',
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural ='Тэги'

    def __str__(self):
        return self.name
