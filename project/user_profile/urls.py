# user_profile/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('get_cert/<str:course_name>/<int:user_id>/', views.get_certificate, name='get_certificate'),
]
