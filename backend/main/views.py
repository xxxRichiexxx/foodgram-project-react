from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.db import models
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rest_framework.decorators import action

from .models import Recipe, RecipeIngredients
from .serializers import RecipeGetSerialiser, RecipeCreateSerializer
from .permissions import ReadOnlyPermission, CreateAndUpdatePermission
from .filters import RecipesFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (ReadOnlyPermission|CreateAndUpdatePermission,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipesFilter

    SERIALIZERS = {
        'list': RecipeGetSerialiser,
        'retrieve': RecipeGetSerialiser,
        'create': RecipeCreateSerializer,
        'update': RecipeCreateSerializer,
        'partial_update': RecipeCreateSerializer,
    }

    def get_serializer_class(self):
        return self.SERIALIZERS[self.action]

    def execution(self, request, pk, attr):
        user = request.user
        try:
            recipe = Recipe.objects.get(id=pk)
        except ObjectDoesNotExist:
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
        return self.execution(request, pk, 'favorite_recipes')

    @action(
        detail=True,
        methods=['post', 'delete'],
    )
    def shopping_cart(self, request, pk):
        return self.execution(request, pk, 'shopping_list')


    @action(['GET'], detail=False)
    def download_shopping_cart(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
        p = canvas.Canvas(response)
        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
        p.setFont('FreeSans', 32)
        p.drawString(150, 800, "Список покупок:")
        user = request.user
        ingredients = RecipeIngredients.objects.filter(recipe_id__buyers__id=user.id).values('ingredient_id__name').annotate(count=models.Sum('amount'), measurement_unit=models.F('ingredient_id__measurement_unit'))
        x, y = 60, 750
        for ingredient in ingredients:
            p.drawString(
                x, y,
                f"- {ingredient['ingredient_id__name']} ({ingredient['measurement_unit']}) - {ingredient['count']}"
            )
            y -= 30
        p.showPage()
        p.save()
        return response