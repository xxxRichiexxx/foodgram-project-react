from django.db import models
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch
from django.db.models import Exists, OuterRef
from django.db.models import Value as V

from .filters import RecipesFilter
from .models import Recipe, RecipeIngredients
from .permissions import CreateAndUpdatePermission, ReadOnlyPermission
from .serializers import RecipeCreateSerializer, RecipeGetSerialiser


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Представление для реализации основных действий с рецептами:
    - создание
    - получение списка
    - детализация
    - редактирование
    - удаление
    """
    queryset = Recipe.objects.select_related('author_id').prefetch_related(
        'tags',
        Prefetch(
            'recipe_ingredients',
            queryset=RecipeIngredients.objects.select_related('ingredient_id')
        )
    )
    permission_classes = (ReadOnlyPermission | CreateAndUpdatePermission,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipesFilter

    SERIALIZERS = {
        'list': RecipeGetSerialiser,
        'retrieve': RecipeGetSerialiser,
        'create': RecipeCreateSerializer,
        'update': RecipeCreateSerializer,
        'partial_update': RecipeCreateSerializer,
    }

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            is_favorited_query = user.favorite_recipes.filter(
                id=OuterRef('pk')
            )
            is_in_shopping_cart_query = user.shopping_list.filter(
                id=OuterRef('pk')
            )
            return Recipe.objects.annotate(
                is_favorited=Exists(is_favorited_query),
                is_in_shopping_cart=Exists(is_in_shopping_cart_query),
            )
        return Recipe.objects.annotate(
            is_favorited=V(False),
            is_in_shopping_cart=V(False),
        )

    def get_serializer_class(self):
        return self.SERIALIZERS[self.action]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            RecipeGetSerialiser(
                obj,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def execution(self, request, pk, attr):
        user = request.user
        try:
            recipe = Recipe.objects.get(id=pk)
        except Recipe.DoesNotExist:
            data = {
                "errors": "рецепта не существует"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data = {
            "id": recipe.id,
            "name": recipe.name,
            "image": recipe.image.url,
            "cooking_time": recipe.cooking_time,
        }
        if request.method == 'DELETE':
            getattr(user, attr).remove(recipe)
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        getattr(user, attr).add(recipe)
        return Response(data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['post', 'delete'],
    )
    def favorite(self, request, pk):
        """Добавление рецепта в избранное, удаление."""
        return self.execution(request, pk, 'favorite_recipes')

    @action(
        detail=True,
        methods=['post', 'delete'],
    )
    def shopping_cart(self, request, pk):
        """Добавление рецепта в список покупок, удаление."""
        return self.execution(request, pk, 'shopping_list')

    @action(['GET'], detail=False)
    def download_shopping_cart(self, request):
        """Скачивание списка покупок."""
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="somefilename.pdf"')
        p = canvas.Canvas(response)
        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
        p.setFont('FreeSans', 32)
        p.drawString(150, 800, "Список покупок:")
        user = request.user
        ingredients = RecipeIngredients.objects.filter(
            recipe_id__buyers__id=user.id
        ).values('ingredient_id__name').annotate(
            count=models.Sum('amount'),
            measurement_unit=models.F('ingredient_id__measurement_unit')
        )
        x, y = 60, 750
        for ingredient in ingredients:
            p.drawString(
                x, y,
                f"""- {ingredient['ingredient_id__name']} ({ingredient['measurement_unit']})
                 - {ingredient['count']}"""
            )
            y -= 30
        p.showPage()
        p.save()
        return response
