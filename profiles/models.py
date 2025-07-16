from django.db import models
from accounts.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name="profile")
    full_name = models.CharField(max_length=150)
    bio = models.TextField(max_length=1024 , null=True , blank=True)
    hourly_rate = models.DecimalField(max_digits=10 , decimal_places=2, null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name

