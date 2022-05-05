from django.contrib import admin


from .models import Recipe, Ingredient, ShoppingList, RecipeIngredients


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    pass
