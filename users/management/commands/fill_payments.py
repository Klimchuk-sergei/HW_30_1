from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from course.models import Course
from users.models import Payment
from lesson.models import Lesson
from decimal import Decimal
import random
from datetime import datetime, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = "Заполняем базу данных тестовыми платежами"

    def handle(self, *arg, **options):
        """Очищаем поля платежей"""
        Payment.objects.all().delete()
        self.stdout.write("Старые платежи удалены.")

        """Получаем нужные обёекты из БД"""
        users = list(User.objects.all())
        courses = list(Course.objects.all())
        lessons = list(Lesson.objects.all())

        if not users or not (courses or lessons):
            self.stdout.write(
                self.style.ERROR("Недостаточно данных для создания платежей")
            )
            return

        payments_to_create = []

        """Создаем платежи"""

        for i in range(20):
            user = random.choice(users)

            # Рандомно выбираем оплата курса или урока
            if courses and random.choice([True, False]):
                paid_course = random.choice(courses)
                paid_lesson = None
                amount = Decimal(random.randint(1000, 20000))
            elif lessons:
                paid_course = None
                paid_lesson = random.choice(lessons)
                amount = Decimal(random.randint(500, 5000))
            else:
                continue

            """ Рандомная дата за последние 300 дней"""
            random_date = (
                datetime.now()
                + timedelta(days=random.randint(-300, 300))
                - timedelta(days=random.randint(0, 30))
            )

            payment = Payment(
                user=user,
                paid_course=paid_course,
                paid_lesson=paid_lesson,
                amount=amount,
                payment_method=random.choice([Payment.CASH, Payment.TRANSFER]),
            )

            payment.payment_date = random_date
            payments_to_create.append(payment)

        Payment.objects.bulk_create(payments_to_create)
        self.stdout.write(
            self.style.SUCCESS(f"Успешно создано {len(payments_to_create)}")
        )
