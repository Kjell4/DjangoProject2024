from django.contrib import admin
from django.urls import path, include
from django.shortcuts import HttpResponse
from courses.views import home, coursePage, SignupView, login
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

urlpatterns = [
    path('', home, name = 'home'),
    path('signup/', SignupView.as_view(), name = 'signup'),
    path('login/', login, name = 'login'),
    path('course/<str:slug>', coursePage, name = 'coursepage'),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)