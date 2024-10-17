# exam/urls.py
from django.urls import path
from .views import take_test

urlpatterns = [
    path('take_test/<slug:slug>/', take_test, name='take_test'),  # Используем slug
]
