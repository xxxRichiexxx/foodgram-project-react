from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from .models import Ingredient
from .filters import IngredientsSearchFilter
from .serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для получения списка и детализации по Ингредиентам."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend, IngredientsSearchFilter)
    pagination_class = None
