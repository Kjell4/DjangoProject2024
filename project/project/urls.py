from django.contrib import admin
from django.urls import path, include
from teacher.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("courses.urls")),
    path('', include('user_payment.urls')),
    path('exam/', include('exam.urls')),
    path('user/', include('user_profile.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('teacher/', include('teacher.urls')),
    
    
]
