from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Djoser authentication endpoints:
    path('api/auth/', include('djoser.urls')),       # register, users, password reset, etc.
    path('api/auth/', include('djoser.urls.jwt')),   # jwt/create (login), jwt/refresh

    # Your app routes (moved to 'projects/' to avoid conflict)
    path("api/", include("projects.urls")),
]
