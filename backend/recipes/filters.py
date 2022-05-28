import django_filters

from tags.models import Tag

from .models import Recipe


class RecipesFilter(django_filters.FilterSet):
    """Фильтрация рецептов."""
    author = django_filters.CharFilter(field_name='author_id')
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = django_filters.BooleanFilter(
        method='get_is_favorited',
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='get_is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if not value:
            return queryset
        return queryset.filter(connoisseurs__id=user.id)

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == 1:
            return queryset.filter(buyers__id=user.id)
        return queryset.exclude(buyers__id=user.id)
