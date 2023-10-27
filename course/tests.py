from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from .models import Lesson, Course, Subscription


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.course = Course.objects.create(
            title='Test course',
            description='Test course description'
        )

        self.lesson = Lesson.objects.create(
            title='Test lesson',
            description='Test lesson description',
            url='https://www.youtube.com/testlesson',
            course=self.course
        )

    def test_get_list_lessons(self):
        user = User.objects.create_user(email='testuser@example.ru', password='testpassword')
        self.client.force_authenticate(user=user)

        response = self.client.get(
            reverse('course:lesson_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': 1,
                        'url': 'https://www.youtube.com/testlesson',
                        'title': 'Test lesson',
                        'description': 'Test lesson description',
                        'preview': None,
                        'course': self.lesson.course_id
                    }
                ]
            }
        )

    def test_lesson_create(self):
        user = User.objects.create_user(email='test2user@example.ru', password='test2password')
        self.client.force_authenticate(user=user)

        data = {
            'title': 'Test lesson2',
            'description': 'Test lesson2 Description',
            'course': self.course.id,
            'url': 'https://www.youtube.com/testlesson'
        }

        response = self.client.post(
            reverse('course:lesson_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_lesson_retrieve(self):
        user = User.objects.create_user(email='test3user@example.ru', password='test3password')
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('course:lesson_get', args=[self.lesson.id]))
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_update(self):
        user = User.objects.create_user(email='test4user@example.ru', password='test4password')
        self.client.force_authenticate(user=user)

        data = {
            'title': 'Updated lesson',
            'description': 'Updated lesson Description',
            'course': self.course.id,
            'url': 'https://www.youtube.com/updatedlesson'
        }

        response = self.client.put(
            reverse('course:lesson_update', args=[self.lesson.id]),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_destroy(self):
        user = User.objects.create_user(email='test5user@example.ru', password='test5password')
        self.client.force_authenticate(user=user)

        response = self.client.delete(reverse('course:lesson_delete', args=[self.lesson.id]))
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionCourseTestCase(APITestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title='Test course',
            description='Test course description'
        )

        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )

        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course
        )

    def test_subscription_course_create(self):
        user = User.objects.create_user(email='test6user@example.ru', password='test6password')
        self.client.force_authenticate(user=user)

        response = self.client.post(
            reverse('course:subscription_create', args=[self.course.id])
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['detail'], 'Подписка на данный курс выполнена успешно!')

    def test_subscription_course_create_already_subscribed(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('course:subscription_create', args=[self.course.id])
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Вы уже подписаны на данный курс!')

    def test_subscription_course_destroy(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse('course:subscription_delete', args=[self.course.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Вы успешно отписались от данного курса!')
