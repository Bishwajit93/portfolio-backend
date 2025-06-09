from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length = 200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=250)
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    
    def __str__(self):
        return self.title