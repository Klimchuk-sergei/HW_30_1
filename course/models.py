from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    course_image = models.ImageField(
        upload_to="courses/images/", blank=True, null=True, verbose_name="Course Image"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Owner"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class Subscription(models.Model):
    """модель подписки на курс"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscriptions",
    )
    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        verbose_name="курс",
        related_name="subscriptions",
    )
    subscribed_at = models.DateTimeField(
        auto_now_add=True, verbose_name="дата подписки"
    )

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        unique_together = ["user", "course"]  # Одна подписка на пользователя и на курс

    def __str__(self):
        return f"{self.user.email} подписан на {self.course.title}"
