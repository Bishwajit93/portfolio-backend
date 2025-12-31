from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


User = get_user_model()


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not current_password or not new_password:
            return Response({"detail": "Missing data."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        if not user.check_password(current_password):
            return Response({"detail": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        if current_password == new_password:
            return Response({"detail": "New password must be different."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password, user=user)
        except Exception as e:
            return Response(
                {"detail": "Password validation failed.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        # Invalidate all refresh tokens for this user
        try:
            for token in OutstandingToken.objects.filter(user=user):
                BlacklistedToken.objects.get_or_create(token=token)
        except Exception as e:
            return Response(
                {
                    "detail": "Password updated but token invalidation failed.",
                    "error": str(e),
                    "debug": {
                        "blacklist_app_installed": True,
                        "user_id": user.pk,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response({"detail": "Password updated. Please log in again."}, status=status.HTTP_200_OK)


class ChangeEmailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_email = request.data.get("new_email")
        if not new_email:
            return Response({"detail": "Missing data."}, status=status.HTTP_400_BAD_REQUEST)

        new_email = new_email.strip().lower()

        if User.objects.filter(email=new_email).exclude(pk=request.user.pk).exists():
            return Response({"detail": "This email is already in use."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user.email = new_email
        user.save()

        return Response({"detail": "Email updated."}, status=status.HTTP_200_OK)


class ChangeUsernameAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_username = request.data.get("new_username")
        if not new_username:
            return Response({"detail": "Missing data."}, status=status.HTTP_400_BAD_REQUEST)

        new_username = new_username.strip()

        if User.objects.filter(username=new_username).exclude(pk=request.user.pk).exists():
            return Response({"detail": "This username is already taken."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user.username = new_username
        user.save()

        return Response({"detail": "Username updated."}, status=status.HTTP_200_OK)
