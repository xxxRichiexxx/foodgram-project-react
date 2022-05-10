from djoser.views import UserViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from .serializers import CustomUserSerializer


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
            self.permission_classes = (self.PERMISSION_PATTERNS[self.action],)
            return super(UserViewSet, self).get_permissions()
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
            data = {
                "errors": "автора не существует"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data = {
            "id": author.id,
            "email": author.email,
        }
        if request.method == 'DELETE':
            user.authors.remove(author)
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        user.authors.add(author)
        return Response(data, status=status.HTTP_201_CREATED)

    @action(['get'], detail=False)
    def subscriptions(self, request):
        user = request.user
        self.queryset = user.authors.all()
        return self.list(self, request)


    # FORBIDDEN_METHODS = (
    #     'activation', 'resend_activation', 'reset_password',
    #     'reset_password_confirm', 'set_username', 'reset_username',
    #     'reset_username_confirm',
    # )

    # def __getattribute__(self, name):
    #     if name in self.FORBIDDEN_METHODS:
    #         raise AttributeError('no such method')
    #     return super().__getattribute__(name)







