from rest_framework import serializers
from .models import Project, Experience, Education, Skill


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

    def validate(self, data):
        status_value = data.get("status")
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        allowed = {"Completed", "In Progress", "Paused"}
        if status_value not in allowed:
            raise serializers.ValidationError({"status": "Invalid status."})

        if status_value == "Completed":
            if not end_date:
                raise serializers.ValidationError({"end_date": "End date is required for completed projects."})
            if start_date and end_date and end_date < start_date:
                raise serializers.ValidationError({"end_date": "End date cannot be before start date."})

        if status_value in {"In Progress", "Paused"}:
            data["end_date"] = None

        return data


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"

    def validate(self, data):
        still_working = data.get("still_working", False)
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        # If frontend sends empty string, normalize it (just in case)
        if end_date == "":
            data["end_date"] = None
            end_date = None

        if still_working:
            data["end_date"] = None
            return data

        if not end_date:
            raise serializers.ValidationError({"end_date": "End date is required if not still working."})

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "End date cannot be before start date."})

        return data


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"

    def validate(self, data):
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "End date cannot be before start date."})

        return data


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"
