from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..models import Experience
from ..serializers import ExperienceSerializer
import traceback

class ExperienceList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        try:
            experiences = Experience.objects.all()
            serializer = ExperienceSerializer(experiences, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("❌ ERROR:", str(e))
            traceback.print_exc()  # 🔥 This line will show the full error in terminal
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ExperienceDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk, require_owner=False, user=None):
        try:
            obj = Experience.objects.get(pk=pk)
            if require_owner and obj.user != user:
                return None
            return obj
        except Experience.DoesNotExist:
            return None

    def get(self, request, pk):
        experience = self.get_object(pk)
        if not experience:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ExperienceSerializer(experience)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        experience = self.get_object(pk, require_owner=True, user=request.user)
        if not experience:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ExperienceSerializer(experience, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        experience = self.get_object(pk, require_owner=True, user=request.user)
        if not experience:
            return Response(status=status.HTTP_404_NOT_FOUND)
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
