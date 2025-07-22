from rest_framework import serializers
from .models import User
from .utils import ROLE_CHOICES


class RegisterSerializer(serializers.Serializer):
    
    
    
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True , min_length=8)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)
    
    

class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)
    
    
    

class UserResponseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["email" , "username" , "role"]