from django.urls import path, include
from rest_framework.routers import DefaultRouter

from djoser.views import TokenCreateView, TokenDestroyView

from .views import CustomUserViewSet


router = DefaultRouter()
router.register('', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/login/', TokenCreateView.as_view(), name="login"),
    path('token/logout/', TokenDestroyView.as_view(), name="logout"),
]
