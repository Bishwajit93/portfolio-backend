from django.urls import path
from .views.projects import ProjectList, ProjectDetail
from .views.experience import ExperienceList, ExperienceDetail
from .views.education import EducationList, EducationDetail
from .views.skill import SkillList, SkillDetail
from .views.auth_custom import (
    CustomTokenObtainPairView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,
)
from .views.email import ContactFormEmailView


urlpatterns = [
    # Auth (JWT login and password reset)
    path("auth/jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("auth/request-reset-password/", PasswordResetRequestAPIView.as_view(), name="request-reset-password"),
    path("auth/reset-password-confirm/", PasswordResetConfirmAPIView.as_view(), name="reset-password-confirm"),

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
