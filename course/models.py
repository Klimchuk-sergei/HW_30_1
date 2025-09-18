from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    course_image = models.ImageField(
        upload_to='courses/images/',
        blank=True,
        null=True,
        verbose_name="Course Image"
    )