# backend/projects/views/auth_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

User = get_user_model()

class RetrieveUsernameView(APIView):
    permission_classes = [AllowAny]

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
            return Response({"username": user.username})
        except User.DoesNotExist:
            return Response(
                {"email": ["No account with that email."]},
                status=status.HTTP_404_NOT_FOUND
            )
