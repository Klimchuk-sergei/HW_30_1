from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(verbose_name="Description")

    course_image = models.ImageField(
        upload_to="courses/images/", blank=True, null=True, verbose_name="Course Image"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
