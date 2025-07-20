from pathlib import Path
import os

# Try importing dotenv and loading .env explicitly
try:
    from dotenv import load_dotenv
except ImportError:
    print("WARNING: python-dotenv is not installed, .env loading will fail!")

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)
    print(f"Loaded environment from {dotenv_path}")
else:
    print(f"WARNING: .env file not found at {dotenv_path}")

import dj_database_url

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'projects',  # Your app here
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS configuration
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://portfoliosite-frontend-lsza.vercel.app",  # Replace with your actual frontend URL
]

# REST framework configuration (JWT Authentication)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# Database configuration (Postgres)
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}

# Static files configuration
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

