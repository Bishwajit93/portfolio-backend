from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Education
from ..serializers import EducationSerializer

class EducationList(APIView):
    
    def get(self, request):
        educations= Education.objects.all()
        serializer=EducationSerializer(educations, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer=EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    

class EducationDetail(APIView):
    
    def get_object(self, pk):
        try:
            return EducationSerializer.objects.get(pk=pk)
        except Education.DoesNotExist:
            return None
    
    def get(self, request, pk):
        education = self.get_object(pk)
        if not education:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EducationSerializer(education)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        education= self.get_object(pk)
        if not education:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EducationSerializer(education, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        education=self.get_object(pk)
        if not Education:
            return Response(status=status.HTTP_404_NOT_FOUND)
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
            