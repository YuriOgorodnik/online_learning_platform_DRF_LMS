from django.conf import settings
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name="название")
    preview = models.ImageField(
        upload_to="course/", verbose_name="превью", null=True, blank=True
    )
    description = models.TextField(verbose_name="описание")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.title} {self.description}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    preview = models.ImageField(
        upload_to="lesson/", verbose_name="превью", null=True, blank=True
    )
    url = models.URLField(verbose_name="ссылка на видео")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="курс")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.title} {self.description}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="пользователь"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="курс")

    def __str__(self):
        return f"Пользователь {self.user.email} подписан на {self.course.title}"

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
