from rest_framework import permissions


class IsAuthorOrModerOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print(request.method in permissions.SAFE_METHODS
                or (request.user.role in ['admin', 'moderator'])
                or obj.author == request.user)
        return (request.method in permissions.SAFE_METHODS
                or (request.user.role in ['admin', 'moderator'])
                or obj.author == request.user)


class IsAdminRoleOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.role == 'admin'))
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.role == 'admin'))
