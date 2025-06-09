# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from.serializers import ProjectSerializer

class ProjectList(APIView):
    def get(self, request):
        projects = Project.objects.all() # get all projects from the database
        serializer = ProjectSerializer(projects, many=True) # convert to JSON
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProjectSerializer(data= request.data) # convert JSON to Python
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        project = Project.objects.get(pk=pk)
        serializer = ProjectSerializer(project, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        project = Project.objects.get(pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)