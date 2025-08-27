from accounts.models import User
from .models import Job
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class JobSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=1024)
    budget = serializers.DecimalField(max_digits=10, decimal_places=2)
    deadline = serializers.DateField()
    category = serializers.CharField(max_length=20, required=False)
    # Additional fields sent by frontend but not stored in model (for now)
    skills_required = serializers.ListField(
        child=serializers.CharField(max_length=100), required=False
    )
    experience_level = serializers.CharField(max_length=50, required=False)
    project_duration = serializers.CharField(max_length=50, required=False)
    job_type = serializers.CharField(max_length=50, required=False)


class JobResponseSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "budget",
            "deadline",
            "category",
            "skills_required",
            "experience_level",
            "project_duration",
            "job_type",
            "client",
            "created_at",
        ]


class JobUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150, required=False)
    description = serializers.CharField(max_length=1024, required=False)
    budget = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    deadline = serializers.DateField(required=False)
    category = serializers.CharField(max_length=20, required=False)
