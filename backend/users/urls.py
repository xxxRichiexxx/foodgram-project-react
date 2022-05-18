from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

app_name = 'auth&users'

router = DefaultRouter()
router.register('', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/login/', TokenCreateView.as_view(), name="login"),
    path('token/logout/', TokenDestroyView.as_view(), name="logout"),
]
