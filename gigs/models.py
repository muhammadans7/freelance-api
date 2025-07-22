from django.db import models
from accounts.models import User

class Gig(models.Model):
    
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE , related_name="gigs")
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=1024)
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    delivery_time = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

