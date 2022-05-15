from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import TagViewSet

app_name = 'tags'

router = DefaultRouter()
router.register('', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]