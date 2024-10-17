from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("courses.urls")),
    path('', include('user_payment.urls')),
    path('exam/', include('exam.urls')),
]
