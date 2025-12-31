from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings


User = get_user_model()


# ========================
# JWT LOGIN VIEW
# ========================
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


def _mail_debug_info():
    return {
        "email_backend": getattr(settings, "EMAIL_BACKEND", ""),
        "email_host": getattr(settings, "EMAIL_HOST", ""),
        "email_port": getattr(settings, "EMAIL_PORT", ""),
        "email_use_tls": getattr(settings, "EMAIL_USE_TLS", ""),
        "from_email": getattr(settings, "DEFAULT_FROM_EMAIL", ""),
        "host_user_present": bool(getattr(settings, "EMAIL_HOST_USER", "")),
        "host_password_present": bool(getattr(settings, "EMAIL_HOST_PASSWORD", "")),
        "frontend_url": getattr(settings, "FRONTEND_URL", ""),
    }


# ========================
# PASSWORD RESET FLOW
# ========================
class PasswordResetRequestAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        email = email.strip().lower()

        # Always return 200 to avoid user enumeration
        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {"detail": "If the email is registered, you will receive a reset link."},
                status=status.HTTP_200_OK,
            )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        try:
            sent_count = send_mail(
                "Reset Your Password",
                f"Click the link below to reset your password:\n\n{reset_link}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            return Response(
                {
                    "detail": "Email sending failed.",
                    "error": str(e),
                    "debug": _mail_debug_info(),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # IMPORTANT: prove if Django actually sent it to SMTP
        return Response(
            {
                "detail": "If the email is registered, you will receive a reset link.",
                "sent_count": sent_count,
                "debug": _mail_debug_info(),
            },
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmAPIView(APIView):
    def post(self, request):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        if not uidb64 or not token or not new_password:
            return Response({"detail": "Missing data."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"detail": "Invalid UID."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)


# ========================
# FORGOT USERNAME FLOW
# ========================
class ForgotUsernameAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        email = email.strip().lower()

        # Always return 200 to avoid user enumeration
        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {"detail": "If the email is registered, your username has been sent."},
                status=status.HTTP_200_OK,
            )

        try:
            sent_count = send_mail(
                "Your Username",
                f"Hello,\n\nYour username is: {user.username}\n\nIf you did not request this, please ignore the email.",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            return Response(
                {
                    "detail": "Email sending failed.",
                    "error": str(e),
                    "debug": _mail_debug_info(),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "detail": "If the email is registered, your username has been sent.",
                "sent_count": sent_count,
                "debug": _mail_debug_info(),
            },
            status=status.HTTP_200_OK,
        )
