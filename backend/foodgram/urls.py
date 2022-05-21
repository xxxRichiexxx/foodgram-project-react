from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


admin.site.site_header = "FOODGRAM"

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'api/users/',
        include('users.urls', namespace='auth&users')
    ),
    path(
        'api/auth/',
        include('users.urls', namespace='auth&users')
    ),
    path(
        'api/tags/',
        include('tags.urls', namespace='tags')
    ),
    path(
        'api/recipes/',
        include('recipes.urls', namespace='recipes')
    ),
    path(
        'api/ingredients/',
        include('ingredients.urls', namespace='ingredients')
    ),
    path(
        'drf-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
