# backend/config/startup.py

from django.apps import AppConfig
import os

class StartupConfig(AppConfig):
    name = "config"  # matches the project folder name

    def ready(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        username = os.getenv("DJANGO_SUPERUSER_NAME")
        email    = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if username and password:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email or ""}
            )
            if not created:
                user.email = email or user.email
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
