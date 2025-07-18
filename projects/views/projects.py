from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Project
from ..serializers import ProjectSerializer
from projects.permissions import IsOwnerOrReadOnly

class ProjectList(APIView):
    
    permission_classes = [IsOwnerOrReadOnly]
    
    def get(self, request):
        projects = Project.objects.filter(user=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetail(APIView):
    
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_object(self, pk, user):
        try:
            return Project.objects.get(pk=pk, user=user)
        except Project.DoesNotExist:
            return None

    def get(self, request, pk):
        project = self.get_object(pk, request.user)
        if not project:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk, request.user)
        if not project:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = self.get_object(pk, request.user)
        if not project:
            return Response(status=status.HTTP_404_NOT_FOUND)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
