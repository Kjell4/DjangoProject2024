from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

class UserPayment(models.Model):
    app_user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь может иметь несколько платежей
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)  # Связь с курсом
    stripe_checkout_id = models.CharField(max_length=255, null=True, blank=True)
    payment_bool = models.BooleanField(default=False)

    def __str__(self):
        return f'Payment info for {self.app_user.username} for course {self.course.title}'


    def __str__(self):
        return f'Payment info for {self.app_user.username} for course {self.course.title}'