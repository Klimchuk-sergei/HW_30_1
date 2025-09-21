from django.db import models
from course.models import Course


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="курс"
    )

    title = models.CharField(max_length=200, verbose_name="title")
    description = models.TextField(verbose_name="description")

    lesson_image = models.ImageField(
        upload_to="lesson/images/", blank=True, null=True, verbose_name="Lesson Image"
    )

    video_file = models.URLField(
        blank=True,
        null=True,
        verbose_name="Video URL",
        help_text="Enter YouTube or Vimeo video URL",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
