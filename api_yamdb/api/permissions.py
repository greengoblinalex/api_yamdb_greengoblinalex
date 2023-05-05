from rest_framework import permissions
from django.urls import reverse


class DoubledPermission(permissions.BasePermission):
    """has_object_permission дублирует логику has_permission"""

    def has_permission(self, request, view):
        raise NotImplementedError()

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class ReadOnly(DoubledPermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdmin(DoubledPermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)


class IsModerator(DoubledPermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_moder)


class IsAuthor(DoubledPermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsSuperuser(DoubledPermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_superuser)


class IsYourself(DoubledPermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if reverse('users-me') in request.build_absolute_uri():
            if request.method in ['GET', 'DELETE']:
                return True
            elif request.method == 'PATCH':
                if 'role' in request.data:
                    return False
                else:
                    return True
        return False
