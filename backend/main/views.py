from rest_framework import viewsets 

from .models import Recipe
from .serializers import RecipeSerialiser


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerialiser
