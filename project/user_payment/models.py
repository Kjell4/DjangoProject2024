from django.db import models
from django.contrib.auth.models import User

class UserPayment(models.Model):
    app_user = models.OneToOneField(User, on_delete=models.CASCADE)  # или ForeignKey, если один пользователь может иметь несколько платежей
    stripe_checkout_id = models.CharField(max_length=255, null=True, blank=True)
    payment_bool = models.BooleanField(default=False)

    def __str__(self):
        return f'Payment info for {self.app_user.username}'