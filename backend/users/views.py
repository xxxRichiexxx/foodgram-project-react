from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import CustomUserSerializer, SubscriptionsSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Представление для модели User, основанное на вьюсете из Djoser."""
    serializer_class = CustomUserSerializer
    http_method_names = ['get', 'post', 'delete']

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
            return [self.PERMISSION_PATTERNS[self.action]()]
        return super().get_permissions()

    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().me(request, *args, **kwargs)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id):
        user = request.user
        try:
            author = User.objects.get(id=id)
        except ObjectDoesNotExist:
            data = {"errors": "автора не существует"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            user.authors.remove(author)
            return Response(status=status.HTTP_204_NO_CONTENT)
        user.authors.add(author)
        data = SubscriptionsSerializer(
            author,
            context=self.get_serializer_context()
            ).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(['get'], detail=False)
    def subscriptions(self, request):
        self.queryset = request.user.authors.all()
        self.serializer_class = SubscriptionsSerializer
        return self.list(self, request)
