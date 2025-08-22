from accounts.models import User
from .models import Gig
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username" , "email"]

class GigSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=1024)
    price = serializers.DecimalField(max_digits=10 , decimal_places=2)
    delivery_time = serializers.IntegerField()
    is_active = serializers.BooleanField(default=True)

class GigResponseSerializer(serializers.ModelSerializer):
    freelancer =  UserSerializer()

    class Meta:
        model = Gig
        fields = ["freelancer" , "title" , "description" , "price" , "delivery_time" , "is_active"]

class UpdateGigSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150, required=False)
    description = serializers.CharField(max_length=1024, required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    delivery_time = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)

