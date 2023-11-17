from django.db import models
from users.models import User


class Payment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="пользователь"
    )
    date = models.DateField(verbose_name="дата оплаты")
    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="оплаченный курс",
    )
    lesson = models.ForeignKey(
        "course.Lesson",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="оплаченный урок",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="сумма оплаты"
    )

    PAYMENT_METHOD_CHOICES = [
        ("cash", "наличные"),
        ("transfer", "перевод на счет"),
    ]
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="cash",
        verbose_name="способ оплаты",
    )

    def __str__(self):
        return f"{self.user} - {self.date} - {self.amount}"

    class Meta:
        verbose_name = "платёж"
        verbose_name_plural = "платежи"
