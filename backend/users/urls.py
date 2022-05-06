from django.urls import path, include

from .views import login


urlpatterns = [
    path('users/', include('rest_framework.urls')),
    # Djoser создаст набор необходимых эндпоинтов.
    # базовые, для управления пользователями в Django:
    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('auth/', include('djoser.urls.jwt')),
    path('auth/token/login/', login),
]
