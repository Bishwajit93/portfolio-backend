from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Education
from ..serializers import EducationSerializer
from projects.permissions import IsOwnerOrReadOnly

class EducationList(APIView):
    
    permission_classes = [IsOwnerOrReadOnly]
    
    def get(self, request):
        educations= Education.objects.filter(user=request.user)
        serializer=EducationSerializer(educations, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer=EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    

class EducationDetail(APIView):
    
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_object(self, pk, user):
        try:
            return Education.objects.get(pk=pk, user=user)
        except Education.DoesNotExist:
            return None
    
    def get(self, request, pk):
        education = self.get_object(pk, request.user)
        if not education:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EducationSerializer(education)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        education= self.get_object(pk, request.user)
        if not education:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EducationSerializer(education, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        education=self.get_object(pk, request.user)
        if not education:
            return Response(status=status.HTTP_404_NOT_FOUND)
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
            