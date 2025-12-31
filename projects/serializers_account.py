from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        user = self.context["request"].user

        if not user.check_password(data["current_password"]):
            raise serializers.ValidationError({"current_password": "Current password is incorrect."})

        if data["current_password"] == data["new_password"]:
            raise serializers.ValidationError({"new_password": "New password must be different."})

        return data


class ChangeEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField()

    def validate_new_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value


class ChangeUsernameSerializer(serializers.Serializer):
    new_username = serializers.CharField(max_length=150)

    def validate_new_username(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Username cannot be empty.")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value
