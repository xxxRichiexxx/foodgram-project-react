from rest_framework import viewsets
from rest_framework import permissions

from .models import Tag
from .serializers import TagSerialiser


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для получения списка и детализации по Тегам."""
    queryset = Tag.objects.all()
    serializer_class = TagSerialiser
    pagination_class = None
    permission_classes = (permissions.AllowAny,)
    

