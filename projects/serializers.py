from rest_framework import serializers
from .models import Project, Experience, Education, Skill
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def validate(self, data):
        status = data.get("status", "")
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if status == "Completed":
            if not end_date:
                raise serializers.ValidationError({"end_date": "End date is required for completed projects."})
            if start_date and end_date < start_date:
                raise serializers.ValidationError({"end_date": "End date cannot be before start date."})

        elif status == "In Progress":
            data["end_date"] = None  # Forcefully set end_date to None
        else:
            # If status is missing or something else, handle it
            raise serializers.ValidationError({"status": "Invalid status. Must be 'Completed' or 'In Progress'."})

        return data


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

    def validate(self, data):
        still_working = data.get('still_working', False)
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if not still_working:
            if not end_date:
                raise serializers.ValidationError({"end_date": "End date is required if not still working."})
            if start_date and end_date < start_date:
                raise serializers.ValidationError({"end_date": "End date cannot be before start date."})

        return data


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "End date cannot be before start date."})

        return data

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        
        