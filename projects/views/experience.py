from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..models import Experience
from ..serializers import ExperienceSerializer

class ExperienceList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        experiences = Experience.objects.all()
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk, require_owner=True, user=request.user)
        if not experience:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ExperienceSerializer(experience, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        experience = self.get_object(pk, require_owner=True, user=request.user)
        if not experience:
            return Response(status=status.HTTP_404_NOT_FOUND)
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
