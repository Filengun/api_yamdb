from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == 'ADMIN' or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'ADMIN' or request.user.is_superuser)
