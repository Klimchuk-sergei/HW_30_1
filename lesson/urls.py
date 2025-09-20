from django.urls import path
from lesson.views import (
    LessonListAPIView,
    LessonCreateAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
    LessonRetrieveAPIView,
)

app_name = "lesson"
urlpatterns = [
    path("", LessonListAPIView.as_view()),
    path("create/", LessonCreateAPIView.as_view()),
    path("<int:pk>/", LessonRetrieveAPIView.as_view()),
    path("<int:pk>/update/", LessonUpdateAPIView.as_view()),
    path("<int:pk>/delete/", LessonDestroyAPIView.as_view()),
]
