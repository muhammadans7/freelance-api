"""
AI URLs Configuration
URL patterns for AI-powered endpoints
"""

from django.urls import path
from .views import (
    GenerateJobDescriptionView,
    GenerateProposalView,
    PlatformAssistantView,
)

app_name = "ai"

urlpatterns = [
    path(
        "generate-job-description/",
        GenerateJobDescriptionView.as_view(),
        name="generate_job_description",
    ),
    path(
        "generate-proposal/", GenerateProposalView.as_view(), name="generate_proposal"
    ),
    path(
        "platform-assistant/",
        PlatformAssistantView.as_view(),
        name="platform_assistant",
    ),
]
