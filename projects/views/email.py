from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
import resend
import os

# Use environment variable for production
resend.api_key = os.environ.get("RESEND_API_KEY")

class ContactFormEmailView(APIView):
    def post(self, request):
        data = request.data
        name = data.get("name")
        visitor_email = data.get("email")
        message = data.get("message")

        try:
            response = resend.Emails.send({
                "from": "Bishwajit Karmaker (Abdullah) <contact@abdullahstack.com>",      # ✅ Your verified domain
                "to": ["contact@abdullahstack.com","bish.karm123@gmail.com"],                 # ✅ Your Zoho inbox
                "reply_to": [visitor_email],                         # ✅ So you can reply directly
                "subject": f"Portfolio Contact: {name}",
                "html": f"""
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> {visitor_email}</p>
                    <p><strong>Message:</strong><br>{message}</p>
                """
            })

            return Response({"success": True, "data": response}, status=status.HTTP_200_OK)

        except Exception as e:
            print("Email sending failed:", str(e))
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContactFormEmailView(APIView):
    def post(self, request):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        subject = request.data.get("subject")
        message = request.data.get("message")

        if not first_name or not last_name or not email or not subject or not message:
            return Response({"detail": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        full_name = f"{first_name} {last_name}"
        email_subject = f"Portfolio Message: {subject} — from {full_name}"
        email_body = f"""Sender: {full_name} <{email}>

Subject: {subject}

Message:
{message}
"""

        try:
            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            return Response({"detail": "Message sent successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Email failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
