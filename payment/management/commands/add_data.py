from django.core.management.base import BaseCommand
from faker import Faker
import random
from decimal import Decimal

from course.models import Lesson, Course
from payment.models import Payment
from users.models import User

fake = Faker()


class Command(BaseCommand):
    """
        Команда для сброса и добавления тестовых данных в модель Payment.

        Метод `handle` выполняет следующие шаги:
        1. Удаляет все записи в моделях Payment, Lesson и Course.
        2. Создает 5 пользователей и сохраняет их в список.
        3. Создает 5 курсов и для каждого курса создает 3 урока.
        4. Создает 20 случайных платежей, связанных с пользователями, курсами и уроками.

        Attributes:
            help (str): Описание команды для вывода при запуске `python manage.py help`.
    """
    help = 'Reset and add sample payment data to the Payment model'

    def handle(self, *args, **kwargs):

        Payment.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()

        users = []
        for _ in range(5):
            email = fake.email()
            phone = fake.numerify()
            city = fake.city()
            user = User.objects.create(email=email, phone=phone, city=city)
            users.append(user)

        courses = []
        lessons = []
        for _ in range(5):
            course = Course.objects.create(
                title=fake.word(),
                description=fake.text(),
            )
            courses.append(course)

            for _ in range(3):
                lesson = Lesson.objects.create(
                    title=fake.sentence(),
                    description=fake.text(),
                    course=course,
                    url=fake.url(),
                )
                lessons.append(lesson)

        for _ in range(20):
            user = random.choice(users)
            payment_date = fake.date_between(start_date='-30d', end_date='today')
            amount = Decimal(random.uniform(10, 100))
            payment_method = random.choice(['cash', 'transfer'])

            is_course = random.choice([True, False])
            course_or_lesson = random.choice(courses) if is_course else random.choice(lessons)

            Payment.objects.create(
                user=user,
                date=payment_date,
                course=course_or_lesson if is_course else None,
                lesson=course_or_lesson if not is_course else None,
                amount=amount,
                payment_method=payment_method,
            )
