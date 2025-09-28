from .models import Course
from .serializers import CourseSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsModerator, IsOwner, IsOwnerOrStaff


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [
                IsAuthenticated,
                ~IsModerator,
            ]  # Модераторы не могут создавать
        elif self.action == "list":
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["retrieve", "update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == "destroy":
            self.permission_classes = [
                IsAuthenticated,
                IsOwner & ~IsModerator,
            ]  # Только владелец и не модератор
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name="Модераторы").exists():
                return Course.objects.all()  # Модераторы видят все курсы
            else:
                return Course.objects.filter(
                    owner=self.request.user
                )  # Обычные пользователи - только свои
        return Course.objects.none()
