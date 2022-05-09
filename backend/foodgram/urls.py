from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/auth/', include('users.urls')),
    path('api/tags/', include('tags.urls')),
    path('api/recipes/', include('main.urls')),
    path('api/ingredients/', include('ingredients.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT) 