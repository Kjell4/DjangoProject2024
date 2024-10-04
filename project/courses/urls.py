from django.contrib import admin
from django.urls import path, include
from django.shortcuts import HttpResponse
from courses.views import home
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home, name='home')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
