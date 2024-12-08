from django.contrib import admin
from django.urls import path, include
from teacher.views import CustomLoginView
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny


swagger_jwt_token = openapi.Parameter(
    'Authorization', in_=openapi.IN_HEADER, type=openapi.TYPE_STRING,
    description="Введите токен в формате `Bearer <your_token>` для авторизации"
)

schema_view = get_schema_view(
   openapi.Info(
      title="Your API",
      default_version='v1',
      description="Описание вашего API, можно указать подробности, такие как методы, примеры, и т.д.",
      terms_of_service="https://www.google.com/policies/terms/",  
      contact=openapi.Contact(email="contact@yourapi.com"),  
      license=openapi.License(name="BSD License"),  
   ),
   public=True,
   permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("courses.urls")),
    path('', include('user_payment.urls')),
    path('exam/', include('exam.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('user/', include('user_profile.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('teacher/', include('teacher.urls')),
    
    
    
]
