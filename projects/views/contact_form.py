# views/contact_form.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import resend
import os

# Set your Resend API key from environment variable
resend.api_key = os.environ.get("RESEND_API_KEY")

class ContactFormEmailView(APIView):
    def post(self, request):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        subject = request.data.get("subject")
        message = request.data.get("message")

        if not all([first_name, last_name, email, subject, message]):
            return Response({"detail": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = resend.Emails.send({
                "from": "Abdullah Portfolio <contact@abdullahstack.com>",
                "to": ["contact@abdullahstack.com", "bish.karm123@gmail.com"],
                "reply_to": [email],
                "subject": f"Portfolio Contact - {subject}",
                "html": f"""
                    <p><strong>From:</strong> {first_name} {last_name} &lt;{email}&gt;</p>
                    <p><strong>Subject:</strong> {subject}</p>
                    <p><strong>Message:</strong><br>{message}</p>
                """,
            })
            return Response({"detail": "Message sent successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            print("Resend Error:", e)
            return Response({"detail": "Failed to send message. Please try again later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
