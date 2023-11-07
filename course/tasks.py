from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from course.models import Subscription, Course
from users.models import User


@shared_task
def send_email_course_update(course_pk):
    subscribers = Subscription.objects.filter(course=course_pk, status=True)
    course = Course.objects.get(pk=course_pk)
    for subscriber in subscribers:
        send_mail(
            subject=f'Внимание! Наш курс {course} обновлён.',
            message='В данном курсе появились новые материалы',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscriber.user.email],
            fail_silently=False
        )


def user_activity_check():
    users = User.objects.all()
    for user in users:
        if user.last_login:
            if timezone.now() - user.last_login > timedelta(days=30):
                user.is_active = False
                user.save()
