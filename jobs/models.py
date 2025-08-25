from django.db import models
from accounts.models import User


class Job(models.Model):
    CATEGORY_CHOICES = [
        ("development", "Development"),
        ("design", "Design"),
        ("writing", "Writing"),
        ("marketing", "Marketing"),
        ("other", "Other"),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=1024)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="other"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.client.username}"
