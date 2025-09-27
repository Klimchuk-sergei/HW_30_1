from django.db import models
from course.models import Course
from django.conf import settings


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="курс"
    )
    title = models.CharField(max_length=200, verbose_name="title")
    description = models.TextField(verbose_name="description")
    preview = models.ImageField(
        upload_to="lesson_previews/",
        blank=True,
        null=True,
        verbose_name="Lesson Image"
    )
    video_file = models.URLField(
        blank=True,
        null=True,
        verbose_name="Video URL",
        help_text="Enter YouTube or Vimeo video URL",
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="owner")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
