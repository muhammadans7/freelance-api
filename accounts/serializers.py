from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.Serializer):
    
    ROLE_CHOICES = (
        ("user" , "User"),
        ("freelancer" , "Freelancer"),
        ("client" , "CLient")
    )
    
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