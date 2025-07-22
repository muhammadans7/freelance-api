from accounts.models import User
from .models import Job
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username" , "email"]


# this will validate incoming data
class JobSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=1024)
    budget = serializers.DecimalField(max_digits=10 , decimal_places=2)
    deadline = serializers.DateField()


# this will return repsonse in Json
class JobResponseSerializer(serializers.ModelSerializer):

    # client = UserSerializer()

    class Meta:
        model = Job
        fields = ["title" , "description" , "budget" , "deadline"]

# for update
class JobUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150, required=False)
    description = serializers.CharField(max_length=1024, required=False)
    budget = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    deadline = serializers.DateField(required=False)
