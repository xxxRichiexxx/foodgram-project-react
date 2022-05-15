from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls', namespace='auth&users')),
    path('api/auth/', include('users.urls', namespace='auth&users')),
    path('api/tags/', include('tags.urls', namespace='tags')),
    path('api/recipes/', include('main.urls', namespace='recipes')),
    path('api/ingredients/', include('ingredients.urls', namespace='ingredients')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT) 