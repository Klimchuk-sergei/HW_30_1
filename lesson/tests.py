from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from lesson.models import Lesson
from course.models import Course


class LessonTestCase(APITestCase):
    def setUp(self):
        # Создаем обычнго пользователя
        self.user = User.objects.create(
            email="testuser@example.com", phone_number="+79991234567"
        )
        self.user.set_password("testpasword123")
        self.user.save()

        # Создаем модератора
        self.moderator = User.objects.create(
            email="moderator@example.com", phone_number="+79991234568"
        )
        self.moderator.set_password("testpassword123")
        self.moderator.save()

        # Создаем другого пользователя
        self.other_user = User.objects.create(
            email="other@example.com", phone_number="+79991234569"
        )
        self.other_user.set_password("testpassword123")
        self.other_user.save()

        # Создаем курс
        self.course = Course.objects.create(
            title="Test Course", description="Test Description", owner=self.user
        )

        # Создаем урок
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Test Lesson Description",
            course=self.course,
            video_file="https://www.youtube.com/watch?v=test123",
            owner=self.user,
        )

    def test_lesson_list_authenticated(self):
        """Тест получения списка уроков авторизованным пользователем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("lesson:lesson-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_list_unauthenticated(self):
        """Тест получения списка уроков неавторизованным пользователем"""
        response = self.client.get(reverse("lesson:lesson-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_create_authenticated(self):
        """Тест создания урока авторизованным пользователем"""
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "New Lesson",
            "description": "New Lesson Description",
            "course": self.course.id,
            "video_file": "https://www.youtube.com/watch?v=new123",
        }
        response = self.client.post(reverse("lesson:lesson-create"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_create_invalid_url(self):
        """Тест создания урока с невалидной ссылкой"""
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "New Lesson",
            "description": "New Lesson Description",
            "course": self.course.id,
            "video_file": "https://vk.com/video123",  # Не YouTube ссылка
        }
        response = self.client.post(reverse("lesson:lesson-create"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_update_owner(self):
        """Тест обновления урока владельцем"""
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Updated Lesson",
            "description": "Updated Description",
            "course": self.course.id,
            "video_file": "https://www.youtube.com/watch?v=updated123",
        }
        response = self.client.put(
            reverse("lesson:lesson-update", kwargs={"pk": self.lesson.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_delete_owner(self):
        """Тест удаления урока владельцем"""
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse("lesson:lesson-delete", kwargs={"pk": self.lesson.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
