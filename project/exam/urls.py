from django.urls import path
from . import views



urlpatterns = [
    path('take_test/<slug:slug>/', views.take_test, name='take_test'),
]