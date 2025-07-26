from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

User = get_user_model()


class PasswordResetRequestAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.filter(email=email).first()
            if not user:
                raise User.DoesNotExist
        except User.DoesNotExist:
            return Response({"detail": "If the email is registered, you will receive a reset link."},
                            status=status.HTTP_200_OK)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        send_mail(
            subject="Reset Your Password",
            message=f"Click the link to reset your password:\n\n{reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response({"detail": "If the email is registered, you will receive a reset link."},
                        status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(APIView):
    def post(self, request):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        if not uidb64 or not token or not new_password:
            return Response({"detail": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Invalid UID."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
