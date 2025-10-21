from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .paginators import CoursePaginator
from .models import Course, Subscription
from django.shortcuts import get_object_or_404
from .serializers import CourseSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsModerator, IsOwner
from drf_spectacular.utils import extend_schema
from users.tasks import send_course_update_email


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

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

    def perform_update(self, serializer):
        instance = serializer.save()

        send_course_update_email.delay(instance.id)
        print(f"Update notification sent for course: {instance.title}")


class SubscriptionAPIView(APIView):
    """APIView для управления подпиской на курс"""

    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Управление подпиской на курс")
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")

        if not course_id:
            return Response(
                {"error": "course_id обязателен"}, status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)
        subscription = Subscription.objects.filter(course=course, user=user)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(course=course, user=user)
            message = "Подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)
