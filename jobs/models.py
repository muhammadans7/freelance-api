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

    EXPERIENCE_LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("expert", "Expert"),
    ]

    PROJECT_DURATION_CHOICES = [
        ("short_term", "Short Term (1-30 days)"),
        ("medium_term", "Medium Term (1-3 months)"),
        ("long_term", "Long Term (3+ months)"),
    ]

    JOB_TYPE_CHOICES = [
        ("fixed_price", "Fixed Price"),
        ("hourly", "Hourly Rate"),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=1024)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="other"
    )
    skills_required = models.JSONField(default=list, blank=True)
    experience_level = models.CharField(
        max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, default="intermediate"
    )
    project_duration = models.CharField(
        max_length=20, choices=PROJECT_DURATION_CHOICES, default="medium_term"
    )
    job_type = models.CharField(
        max_length=20, choices=JOB_TYPE_CHOICES, default="fixed_price"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.client.username}"
