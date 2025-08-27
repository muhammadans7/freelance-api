from accounts.models import User
from jobs.models import Job
from profiles.models import Profile
from .models import Proposal
from rest_framework import serializers
from .utils import STATUS_CHOICE


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["bio", "skills", "hourly_rate", "experience_level"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "profile"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Handle case where user doesn't have a profile
        if not hasattr(instance, "profile"):
            data["profile"] = None
        return data


class JobSerializer(serializers.ModelSerializer):
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
            "client",
        ]


class ProposalSerializer(serializers.Serializer):
    cover_letter = serializers.CharField(max_length=1024)
    proposed_rate = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False
    )
    status = serializers.ChoiceField(choices=STATUS_CHOICE, required=False)


class ProposalResponseSerializer(serializers.ModelSerializer):
    freelancer = UserSerializer()
    job = JobSerializer()

    class Meta:
        model = Proposal
        fields = [
            "id",
            "freelancer",
            "job",
            "cover_letter",
            "proposed_rate",
            "status",
            "created_at",
        ]
