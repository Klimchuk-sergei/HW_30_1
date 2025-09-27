from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group

class IsModerator(BasePermission):
    """Проверка пользователя на модератора"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.groups.filter(name='Модераторы').exits()

class IsOwner(BasePermission):
    def has_object_permisssion(selfself, request, view, obj):
        return obj.owner == request.user

class IsOwnerOrStaff(BasePermission):
    """Проверяем, является ли пользователь владельцем обьекта или администратором"""
    def has_object_permission(selfself, request, view, obj):
        if request.user.is_staff:
            return True
        return obj == request.user
    def has_permission(self, request, view):
        return request.user.is_authenticated

