from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from course.models import Course, Subscription


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        """
        Подготовка данных для тестов подписок
        """
        # Создаем пользователя
        self.user = User.objects.create(
            email='testuser@example.com',
            phone_number='+79991234567'
        )
        self.user.set_password('testpassword123')
        self.user.save()

        # Создаем курс
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )

    def test_subscription_create(self):
        """
        Тест создания подписки
        """
        self.client.force_authenticate(user=self.user)
        data = {'course_id': self.course.id}
        response = self.client.post(
            reverse('course:subscription'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(
            user=self.user,
            course=self.course
        ).exists())

    def test_subscription_delete(self):
        """
        Тест удаления подписки
        """
        # Сначала создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)
        data = {'course_id': self.course.id}
        response = self.client.post(
            reverse('course:subscription'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(
            user=self.user,
            course=self.course
        ).exists())

    def test_subscription_without_course_id(self):
        """
        Тест подписки без course_id
        """
        self.client.force_authenticate(user=self.user)
        data = {}
        response = self.client.post(
            reverse('course:subscription'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_subscription_invalid_course_id(self):
        """
        Тест подписки с несуществующим course_id
        """
        self.client.force_authenticate(user=self.user)
        data = {'course_id': 999}  # Несуществующий ID
        response = self.client.post(
            reverse('course:subscription'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_is_subscribed_field(self):
        """
        Тест поля is_subscribed в сериализаторе курса
        """
        # Создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse('course:course-detail', kwargs={'pk': self.course.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])

    def test_is_not_subscribed_field(self):
        """
        Тест поля is_subscribed когда нет подписки
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse('course:course-detail', kwargs={'pk': self.course.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_subscribed'])