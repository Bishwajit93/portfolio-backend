from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from projects.views.auth_custom import CustomLoginAPIView

urlpatterns = [
    path("admin/", admin.site.urls),

    # JWT authentication endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Your app's API routes
    path("api/", include("projects.urls")),
    
    # Custom login page
    path("auth/login/", CustomLoginAPIView.as_view(), name="custom-login")
]
