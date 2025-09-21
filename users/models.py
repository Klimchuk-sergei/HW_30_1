from django.contrib.auth.models import AbstractUser
from django.db import models

from course.models import Course
from lesson.models import Lesson

NULLABLE = {"blank": True, "null": True}


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

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="date created",
    )

    def __str__(self):
        return self.email


class Meta:
    verbose_name = "user"
    verbose_name_plural = "users"


class Payment(models.Model):
    # Способо оплаты
    CASH = "cash"
    TRANSFER = "transfer"
    PAYMENT_METHOD_CHOICES = [
        (CASH, "Cash"),
        (TRANSFER, "Transfer"),
    ]

    # Ссылка на пользователя
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="user",
        related_name="payments",
    )

    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="date payment")

    # ссылка на оплаченый курс (может быть пустым)
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="сумма оплыты",
        related_name="payments",
    )
    # Ссылка на оплаченный урок (может быть пустым)
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="оплаченный урок",
        related_name="payments",
    )

    # Сумма оплаты
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="сумма оплаты"
    )

    # Способ оплаты
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="payment method",
    )

    def __str__(self):
        what_was_paid = ""
        if self.paid_course:
            what_was_paid = self.paid_course.title
        elif self.paid_lesson:
            what_was_paid = {self.paid_lesson.title}
        else:
            what_was_paid = "Не указано"

        return f"{self.user.email} - {what_was_paid} - {self.amount} руб. ({self.get_payment_method_display()}"

    class Meta:
        verbose_name = "payment"
        verbose_name_plural = "payments"
        ordering = ["-payment_date"]
