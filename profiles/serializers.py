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


class ResponseSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        
        fields = ["id", "user", "full_name", "bio", "hourly_rate"]
