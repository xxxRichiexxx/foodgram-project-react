from django.db import models
from django.contrib.auth import get_user_model

from tags.models import Tag

User = get_user_model()

class Ingredient(models.Model):
    """ Модель ингредиентов."""
    name = models.CharField(
        max_length=50,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(max_length=50)

    class Meta:
        verbose_name='Ингредиент'
        verbose_name_plural='Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """" Модель рецептов."""
    author_id = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    picture = models.ImageField(
        verbose_name='Картинка',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient, 
        through='RecipeIngredients',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    preparing_time = models.TimeField()
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    # @property
    # def quantity_in_favorites(self):
    #     return self.connoisseurs.count()

    class Meta:
        default_related_name = 'recipes'
        ordering = ('id', 'title')
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        
    def __str__(self):
        return self.title


class RecipeIngredients(models.Model):
    """" Модель рецепты-ингредиенты."""
    recipe_id = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient_id = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    quantity = models.IntegerField()

    class Meta:
        verbose_name='Рецепт - Ингредиент'
        verbose_name_plural='Рецепты - Ингредиенты'

    def __str__(self):
        return f'{self.recipe_id.title}: {self.ingredient_id.name}'


class ShoppingList(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ShoppingLists',
        verbose_name='Пользователь',
    )
    date = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(
        Recipe,
        related_name='ShoppingLists',
        verbose_name='Рецепты',
    )
    
    class Meta:
        verbose_name='Лист покупок'
        verbose_name_plural='Листы покупок'

    def __str__(self):
        return f'{self.user_id.username}. {self.date}'