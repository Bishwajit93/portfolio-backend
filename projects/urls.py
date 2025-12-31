# projects/urls.py

from django.urls import path
from .views.projects import ProjectList, ProjectDetail
from .views.experience import ExperienceList, ExperienceDetail
from .views.education import EducationList, EducationDetail
from .views.skill import SkillList, SkillDetail
from .views.auth_custom import (
    CustomTokenObtainPairView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,
    ForgotUsernameAPIView,
)
from .views.contact_form import ContactFormEmailView
from .views.account import ChangePasswordAPIView, ChangeEmailAPIView, ChangeUsernameAPIView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # Auth (JWT login and password reset)
    path("auth/jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("auth/request-reset-password/", PasswordResetRequestAPIView.as_view(), name="request-reset-password"),
    path("auth/reset-password-confirm/", PasswordResetConfirmAPIView.as_view(), name="reset-password-confirm"),
    path("auth/forgot-username/", ForgotUsernameAPIView.as_view(), name="forgot-username"),
    path("auth/jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),

    # Account / Security
    path("auth/change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("auth/change-email/", ChangeEmailAPIView.as_view(), name="change-email"),
    path("auth/change-username/", ChangeUsernameAPIView.as_view(), name="change-username"),


    # Projects
    path("projects/", ProjectList.as_view(), name="project-list"),
    path("projects/<int:pk>/", ProjectDetail.as_view(), name="project-detail"),

    # Experience
    path("experiences/", ExperienceList.as_view(), name="experience-list"),
    path("experiences/<int:pk>/", ExperienceDetail.as_view(), name="experience-detail"),

    # Education
    path("educations/", EducationList.as_view(), name="education-list"),
    path("educations/<int:pk>/", EducationDetail.as_view(), name="education-detail"),

    # Skills
    path("skills/", SkillList.as_view(), name="skill-list"),
    path("skills/<int:pk>/", SkillDetail.as_view(), name="skill-detail"),

    # Contact form
    path("contact-form/", ContactFormEmailView.as_view(), name="contact-form"),
]
