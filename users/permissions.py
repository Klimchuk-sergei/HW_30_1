from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Проверка пользователя на модератора"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name="Модераторы").exists()


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrStaff(BasePermission):
    """Проверяем, является ли пользователь владельцем объекта или администратором"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        # Для User объекта
        if hasattr(obj, "owner"):
            return obj.owner == request.user
        # Для самого пользователя (профиль)
        return obj == request.user

    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsOwnerAndNotModerator(BasePermission):
    """Проверяет что пользователь владелец и не модератор"""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        is_owner = obj.owner == request.user
        is_moderator = request.user.groups.filter(name="Модераторы").exists()
        return is_owner and not is_moderator
