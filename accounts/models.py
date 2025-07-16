from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    
    ROLE_CHOICES = (
        ("user" , "User"),
        ("freelancer" , "Freelancer"),
        ("client" , "Client")
    )
    
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES ,default="user")
    
    
    def __str__(self):
        return self.username