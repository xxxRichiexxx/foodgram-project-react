from django.contrib import admin

from .models import Recipe, RecipeIngredients


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('quantity_in_favorites',)
    list_display = ('author_id', 'name')
    search_fields = ('name', 'text')
    list_filter = ('author_id', 'name', 'tags', 'date')

    def quantity_in_favorites(self, instance):
        return instance.connoisseurs.count()

    quantity_in_favorites.short_description = "Количество в избранном"


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_filter = ('recipe_id', )
