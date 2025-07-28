from django.db import models
from accounts.models import User
from jobs.models import Job
from .utils import STATUS_CHOICE

class Proposal(models.Model):
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE , related_name="proposals")
    job = models.ForeignKey(Job , on_delete=models.CASCADE , related_name="proposals")
    cover_letter = models.TextField(max_length=1024)
    proposed_rate = models.DecimalField(max_digits=10 , decimal_places=2 , null=True , blank=True)
    status = models.CharField(max_length=20 , choices=STATUS_CHOICE , default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("freelancer", "job")
        
    
    def __str__(self):
        return f"{self.freelancer.username} → Job #{self.job.id}"