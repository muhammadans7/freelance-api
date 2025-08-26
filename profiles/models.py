from django.db import models
from accounts.models import User

EXPERIENCE_LEVEL_CHOICES = [
    ("beginner", "Beginner"),
    ("intermediate", "Intermediate"),
    ("expert", "Expert"),
]

PROJECT_TYPE_CHOICES = [
    ("short_term", "Short-term"),
    ("long_term", "Long-term"),
    ("part_time", "Part-time"),
    ("full_time", "Full-time"),
]

RESPONSE_TIME_CHOICES = [
    ("within_hour", "Within an hour"),
    ("within_few_hours", "Within a few hours"),
    ("within_day", "Within a day"),
    ("within_few_days", "Within a few days"),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=150)
    bio = models.TextField(max_length=1024, null=True, blank=True)
    hourly_rate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    niche = models.CharField(
        max_length=100, null=True, blank=True, help_text="Main area of expertise"
    )
    skills = models.JSONField(
        default=list, blank=True, help_text="List of technical skills"
    )
    experience_level = models.CharField(
        max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, null=True, blank=True
    )
    years_of_experience = models.PositiveIntegerField(
        null=True, blank=True, help_text="Years of professional experience"
    )
    languages = models.JSONField(default=list, blank=True, help_text="Languages spoken")
    preferred_project_types = models.JSONField(
        default=list, blank=True, help_text="Preferred types of projects"
    )
    minimum_project_budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Minimum budget willing to accept",
    )
    response_time = models.CharField(
        max_length=20, choices=RESPONSE_TIME_CHOICES, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
