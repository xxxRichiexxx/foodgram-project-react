from django_filters import rest_framework as filters

from tags.models import Tag

from .models import Recipe


class RecipesFilter(filters.FilterSet):
    """Фильтрация рецептов."""
    author = filters.CharFilter(field_name='author_id')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = filters.CharFilter(
        method='get_is_favorited',
    )
    is_in_shopping_cart = filters.CharFilter(
        method='get_is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value == '1':
            return queryset.filter(connoisseurs__id=user.id)
        return queryset.exclude(connoisseurs__id=user.id)

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == '1':
            return queryset.filter(buyers__id=user.id)
        return queryset.exclude(buyers__id=user.id)
