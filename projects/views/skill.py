from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Skill
from ..serializers import SkillSerializer
from projects.permissions import IsOwnerOrReadOnly

class SkillList(APIView):
    
    permission_classes = [IsOwnerOrReadOnly]
    
    def get(self, request):
        skills = Skill.objects.filter(user=request.user)
        serializer = SkillSerializer(skills, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer=SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SkillDetail(APIView):
    
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_object(self,pk, user):
        try:
            return Skill.objects.get(pk=pk, user=user)
        except Skill.DoesNotExist:
            return None
        
    def get(self, request, pk):
        skill= self.get_object(pk, request.user)
        if not skill:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer= SkillSerializer(skill)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request,pk):
        skill=self.get_object(pk, request.user)
        if not skill:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=SkillSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        skill = self.get_object(pk, request.user)
        if not skill:
            return Response(status=status.HTTP_404_NOT_FOUND)
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)