from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from config.paginators import CoursePaginator, LessonPaginator
from users.permissions import IsModerator, IsOwner, IsOwnerAndNotModerator
from lesson.models import Lesson
from lesson.serializers import LessonSerializer


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPaginator

    def get_queryset(self):
        if self.request.user.groups.filter(name="Модераторы").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        ~IsModerator,
    ]  # Модераторы не могут создавать

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerAndNotModerator]  # Только владелец и не модератор
    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)