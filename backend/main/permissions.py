from rest_framework import permissions


class ReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS and
                view.action != 'download_shopping_cart')

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class CreateAndUpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.user.is_admin
                or obj.author_id == request.user)
