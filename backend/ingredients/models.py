from django.db import models


class Ingredient(models.Model):
    """ Модель ингредиентов."""
    name = models.CharField(
        max_length=250,
        db_index=True,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единицы измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name
