from django.urls import path
from .views import ProjectList, ProjectDetail

urlpatterns = [
    path('projects/', ProjectList.as_view()),
    path('projects/<int:pk>/', ProjectDetail.as_view()),
]
