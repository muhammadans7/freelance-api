from accounts.models import User
from .models import Job
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class JobSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=1024)
    budget = serializers.DecimalField(max_digits=10, decimal_places=2)
    deadline = serializers.DateField()
    category = serializers.CharField(max_length=20, required=False)


class JobResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["id", "title", "description", "budget", "deadline", "category"]


class JobUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150, required=False)
    description = serializers.CharField(max_length=1024, required=False)
    budget = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    deadline = serializers.DateField(required=False)
    category = serializers.CharField(max_length=20, required=False)
