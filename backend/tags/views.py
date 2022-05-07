from rest_framework import viewsets

from .models import Tag
from .serializers import TagSerialiser


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerialiser
    pagination_class = None

