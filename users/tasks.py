from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from course.models import Course, Subscription
import logging
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


@shared_task
def send_course_update_email(course_id):
    """Уведомление пользователя об обновлении курса"""
    try:
        course = Course.objects.get(id=course_id)
        subscription = Subscription.objects.filter(course=course)

        if not subscription.exists():
            logger.info(f"No subscription for {course.title}")
            return "No subscribe"

        subject = f"Update {course.title}"
        message = f"Update {course.title}"

        email_list = [sub.user.email for sub in subscription if sub.user.email]

        if email_list:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=email_list,
                fail_silently=False,
            )
            logger.info(f"Sent update notifications to {len(email_list)} subscribers")
            return f"Notifications sent to {len(email_list)} subscribers"
        else:
            return "No valid email address"

    except Exception as e:
        logger.error(f"Error sending notifications: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def block_inactive_users():
    """Блокировка пользователя, который не заходил более месяца"""
    try:
        User = get_user_model()
        one_month_ago = timezone.now() - timedelta(days=30)

        # Находим пользователей, которые не заходили больше месяца
        inactive_users = User.objects.filter(
            is_active=True, last_login__lt=one_month_ago
        )

        count = inactive_users.count()

        if count > 0:
            # блокируем пользователей
            inactive_users.update(is_active=False)
            logger.info(f"Inactive users: {count}")
            return f"Inactive users: {count}"
        else:
            logger.error("No active users")
            return "No active users"
    except Exception as e:
        logger.error(f"Error sending notifications: {str(e)}")
        return f"Error: {str(e)}"
