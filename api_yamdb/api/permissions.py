from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                (request.user.role == 'admin' or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'admin' or request.user.is_superuser)


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == 'moderator')

#Мне нужен пермишен без аутотефикации
class IsAdminOrReadOnly(permissions.BasePermission):
    '''
    Редактирование доступно только администратору или супер-пользователю.
    Просмотр доступен всем(и без токена тоже).
    '''
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS 
            or request.user.is_authenticated
            and (request.user.role == 'admin' or request.user.is_superuser)
        )

class IsAuthUserOrAuthorOrModerOrAdmin(permissions.BasePermission):
    '''
    Редактирование доступно авт.пользователям, автору, модератору и админу.
    А всем остальным на просмотр.
    '''
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS 
            or request.user.is_authenticated
            and (
                request.user.role == 'admin' 
                or request.user.is_superuser
                or request.user.role == 'moderator'
                or request.user == obj.author
                or view.action == 'create') #create = POST
        )