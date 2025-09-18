from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="email address", help_text="Email address"
    )
    USERNAME_FIELD = "email"

    phone_number = models.CharField(
        max_length=35,
        unique=True,
        verbose_name="phone number",
        help_text="Phone number",
    )
    sity = models.CharField(
        max_length=300, blank=True, null=True, verbose_name="sity", help_text="You sity"
    )
    avatar = models.ImageField(
        upload_to="avatars",
        blank=True,
        null=True,
        verbose_name="avatar",
        help_text="Avatar",
    )

    REQUIRED_FIELDS = []

class Meta:
    verbose_name = "user"
    verbose_name_plural = "users"