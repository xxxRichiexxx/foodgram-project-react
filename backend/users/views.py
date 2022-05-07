from djoser.views import UserViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return super(UserViewSet, self).get_queryset()

    def get_serializer_class(self):
        if self.action == "me":
            return self.serializer_class
        return super().get_serializer_class()
    
    PERMISSION_PATTERNS = {
        "retrieve": permissions.IsAuthenticated,
        "list": permissions.AllowAny,
    }

    def get_permissions(self):
        if self.action in self.PERMISSION_PATTERNS:
            self.permission_classes = (self.PERMISSION_PATTERNS[self.action],)
            return super(UserViewSet, self).get_permissions()
        return super().get_permissions()   

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().me(request, *args, **kwargs)








