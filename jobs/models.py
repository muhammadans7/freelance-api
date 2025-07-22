from django.db import models
from accounts.models import User
# Create your models here.


class Job(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE , related_name="jobs")
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=1024)
    budget = models.DecimalField(max_digits=10 , decimal_places=2)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} by {self.client.username}"


