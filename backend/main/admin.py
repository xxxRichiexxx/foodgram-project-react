from django.contrib import admin


from .models import Recipe, Ingredient, ShoppingList, RecipeIngredients


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('quantity_in_favorites',)
    list_display = ('author_id', 'title')
    search_fields = ('title', 'description') 
    list_filter = ('author_id', 'title', 'tags', 'date')

    def quantity_in_favorites(self, instance):
        return instance.connoisseurs.count()

    quantity_in_favorites.short_description = "Количество в избранном"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',) 
    list_filter = ('name',)


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    pass
