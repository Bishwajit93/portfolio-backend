# projects/views/debug.py

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os

User = get_user_model()


def _clean(s: str) -> str:
    return (s or "").strip().strip('"').strip("'").strip()

def _authorized(request) -> bool:
    """
    Safe rule:
    - If DEBUG=True (local dev), allow without secret.
    - If DEBUG=False (production), require header secret.
    """
    if getattr(settings, "DEBUG", False):
        return True

    secret = _clean(os.environ.get("DEBUG_SECRET", ""))
    if not secret:
        return False

    incoming = _clean(request.headers.get("X-Debug-Secret", ""))
    return incoming == secret



def _current_db_name() -> str:
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database();")
            row = cursor.fetchone()
            return row[0] if row else "unknown"
    except Exception:
        return "unknown"


class DebugStatusAPIView(APIView):
    """
    GET /api/debug/status/
    Header: X-Debug-Secret: <DEBUG_SECRET>  (required in production)
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        if not _authorized(request):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

        db_name = _current_db_name()

        return Response(
            {
                "ok": True,
                "debug": {
                    "debug_mode": getattr(settings, "DEBUG", False),
                    "allowed_hosts": getattr(settings, "ALLOWED_HOSTS", []),
                    "database_vendor": connection.vendor,
                    "database_name": db_name,
                    "database_host": settings.DATABASES["default"].get("HOST"),
                    "database_user": settings.DATABASES["default"].get("USER"),
                    "database_port": settings.DATABASES["default"].get("PORT"),
                    "frontend_url": getattr(settings, "FRONTEND_URL", ""),
                },
                "email": {
                    "backend": getattr(settings, "EMAIL_BACKEND", ""),
                    "host": getattr(settings, "EMAIL_HOST", ""),
                    "port": getattr(settings, "EMAIL_PORT", ""),
                    "use_tls": getattr(settings, "EMAIL_USE_TLS", ""),
                    "from_email": getattr(settings, "DEFAULT_FROM_EMAIL", ""),
                    "host_user_present": bool(getattr(settings, "EMAIL_HOST_USER", "")),
                    "host_password_present": bool(getattr(settings, "EMAIL_HOST_PASSWORD", "")),
                },
                "users": {
                    "count": User.objects.count(),
                    "first_5": list(
                        User.objects.all().values(
                            "id", "username", "email", "is_staff", "is_superuser"
                        )[:5]
                    ),
                },
            },
            status=status.HTTP_200_OK,
        )


class DebugEmailTestAPIView(APIView):
    """
    POST /api/debug/email-test/
    Header: X-Debug-Secret: <DEBUG_SECRET> (required in production)
    Body: { "to_email": "..." }
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        if not _authorized(request):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

        to_email = (request.data.get("to_email") or "").strip()
        if not to_email:
            return Response({"detail": "to_email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sent = send_mail(
                subject="SMTP TEST - AbdullahStack",
                message="If you received this email, SMTP from Railway is working.",
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                recipient_list=[to_email],
                fail_silently=False,
            )
            return Response(
                {
                    "ok": True,
                    "detail": "send_mail executed.",
                    "django_send_mail_return": sent,  # usually 1 if Django sent it to SMTP
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "ok": False,
                    "detail": "Email sending failed.",
                    "error": str(e),
                    "email_debug": {
                        "backend": getattr(settings, "EMAIL_BACKEND", ""),
                        "host": getattr(settings, "EMAIL_HOST", ""),
                        "port": getattr(settings, "EMAIL_PORT", ""),
                        "use_tls": getattr(settings, "EMAIL_USE_TLS", ""),
                        "from_email": getattr(settings, "DEFAULT_FROM_EMAIL", ""),
                        "host_user_present": bool(getattr(settings, "EMAIL_HOST_USER", "")),
                        "host_password_present": bool(getattr(settings, "EMAIL_HOST_PASSWORD", "")),
                    },
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DebugFindUserByEmailAPIView(APIView):
    """
    POST /api/debug/find-user/
    Header: X-Debug-Secret: <DEBUG_SECRET> (required in production)
    Body: { "email": "..." }
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        if not _authorized(request):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

        email = (request.data.get("email") or "").strip().lower()
        if not email:
            return Response({"detail": "email is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            return Response(
                {"ok": True, "found": False, "detail": "No user with that email."},
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "ok": True,
                "found": True,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser,
                },
            },
            status=status.HTTP_200_OK,
        )
