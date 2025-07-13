from django.urls import path
from .views.projects import ProjectList, ProjectDetail
from .views.experience import ExperienceList, ExperienceDetail
from .views.education import EducationList, EducationDetail
from .views.skill import SkillList, SkillDetail

urlpatterns = [
    # Projects
    path('projects/', ProjectList.as_view()),
    path('projects/<int:pk>/', ProjectDetail.as_view()),

    # Experience
    path('experiences/', ExperienceList.as_view()),
    path('experiences/<int:pk>/', ExperienceDetail.as_view()),

    # Education
    path('educations/', EducationList.as_view()),
    path('educations/<int:pk>/', EducationDetail.as_view()),

    # Skills
    path('skills/', SkillList.as_view()),
    path('skills/<int:pk>/', SkillDetail.as_view()),
]
