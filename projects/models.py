from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length = 200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=250)
    github_frontend_url = models.URLField(blank=True, null=True)
    github_backend_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed'),
            ('Paused', 'Paused')
        ],
        default='In Progress'
    )

    
    def __str__(self):
        return self.title
    
    

class Experience(models.Model):
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    still_working = models.BooleanField(default=False)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
    

class Education(models.Model):
    institution_name = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    grade = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} at {self.institution_name}"


class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=100, blank=True)  # e.g. 'Beginner', 'Intermediate', 'Expert'

    def __str__(self):
        return f"{self.name} ({self.level})" if self.level else self.name
