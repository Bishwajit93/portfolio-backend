from rest_framework import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Skill
from ..serializers import SkillSerializer

class SkillLiist(APIView):
    
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer=SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SkillDetail(APIView):
    
    def get_object(self, request,pk):
        try:
            return Skill.objects.get(pk=pk)
        except Skill.DoesNotExist:
            return None
        
    def get(self, request, pk):
        skill= self.get_object(pk)
        if not skill:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer= SkillSerializer(skill)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request,pk):
        skill=self.get_object(pk)
        if not skill:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=SkillSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        skill = self.get_object(pk)#+
        if not skill:
            return Response(status=status.HTTP_404_NOT_FOUND)
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)