from rest_framework import serializers
from .models import Profile
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "role"]


class ProfileSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    bio = serializers.CharField(max_length=1024, allow_null=True, allow_blank=True)
    hourly_rate = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False
    )
    niche = serializers.CharField(
        max_length=100, required=False, allow_null=True, allow_blank=True
    )
    skills = serializers.ListField(
        child=serializers.CharField(max_length=50), required=False
    )
    experience_level = serializers.ChoiceField(
        choices=[
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
            ("expert", "Expert"),
        ],
        required=False,
        allow_null=True,
    )
    years_of_experience = serializers.IntegerField(required=False, allow_null=True)
    languages = serializers.ListField(
        child=serializers.CharField(max_length=50), required=False
    )
    preferred_project_types = serializers.ListField(
        child=serializers.CharField(max_length=50), required=False
    )
    minimum_project_budget = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    response_time = serializers.ChoiceField(
        choices=[
            ("within_hour", "Within an hour"),
            ("within_few_hours", "Within a few hours"),
            ("within_day", "Within a day"),
            ("within_few_days", "Within a few days"),
        ],
        required=False,
        allow_null=True,
    )


class ResponseSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "full_name",
            "bio",
            "hourly_rate",
            "niche",
            "skills",
            "experience_level",
            "years_of_experience",
            "languages",
            "preferred_project_types",
            "minimum_project_budget",
            "response_time",
        ]
