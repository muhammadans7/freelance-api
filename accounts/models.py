from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import ROLE_CHOICES

# Create your models here.


class User(AbstractUser):   
    role = models.CharField(max_length=20, choices=ROLE_CHOICES ,default="user")
     
    def __str__(self):
        return self.username