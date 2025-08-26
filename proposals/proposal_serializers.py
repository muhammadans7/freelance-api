from accounts.models import User
from jobs.models import Job
from .models import Proposal
from rest_framework import serializers
from .utils import STATUS_CHOICE


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


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
