from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet


app_name = "recipes"


router = DefaultRouter()
router.register('', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]