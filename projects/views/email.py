from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import resend
import os

resend.api_key = os.getenv("RESEND_API_KEY")

class ContactFormEmailView(APIView):
    def post(self, request):
        data = request.data
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        try:
            response = resend.Emails.send({
                "from": "Bishwajit Karmaker (Abdullah) <contact@abdullahstack.com>",
                "to": ["contact@abdullahstack.com"],
                "subject": f"Portfolio Contact: {name}",
                "html": f"""
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Message:</strong><br>{message}</p>
                """
            })

            return Response({"success": True, "data": response}, status=status.HTTP_200_OK)

        except Exception as e:
            print("Email sending failed:", str(e))
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
