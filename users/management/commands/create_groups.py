from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from course.models import Course
from lesson.models import Lesson


class Command(BaseCommand):
    help = "Create moderator group with permissions"

    def handle(self, *args, **options):
        # Создаем группу модераторов
        moderator_group, created = Group.objects.get_or_create(name="Модераторы")

        if created:
            # Получаем разрешения для курсов
            course_content_type = ContentType.objects.get_for_model(Course)
            course_permissions = Permission.objects.filter(
                content_type=course_content_type,
                codename__in=["view_course", "change_course"],
            )

            # Получаем разрешения для уроков
            lesson_content_type = ContentType.objects.get_for_model(Lesson)
            lesson_permissions = Permission.objects.filter(
                content_type=lesson_content_type,
                codename__in=["view_lesson", "change_lesson"],
            )

            # Добавляем разрешения в группу
            moderator_group.permissions.add(*course_permissions, *lesson_permissions)
            moderator_group.save()

            self.stdout.write(
                self.style.SUCCESS(
                    'Группа "Модераторы" создана с правами просмотра и редактирования курсов и уроков'
                )
            )
        else:
            self.stdout.write(self.style.WARNING('Группа "Модераторы" уже существует'))
