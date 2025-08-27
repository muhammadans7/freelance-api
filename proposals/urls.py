from django.urls import path
from .proposal_view import (
    ProposalCreateView,
    MyProposalsView,
    ProposalDetailView,
    JobProposalsView,
    ProposalActionView,
    ClientProposalsOverviewView,
)

urlpatterns = [
    # Freelancer endpoints
    path(
        "jobs/<int:job_id>/proposals/",
        ProposalCreateView.as_view(),
        name="create-proposal",
    ),
    path("my-proposals/", MyProposalsView.as_view(), name="my-proposals"),
    path(
        "proposals/<int:proposal_id>/",
        ProposalDetailView.as_view(),
        name="proposal-detail",
    ),
    # Client endpoints
    path(
        "jobs/<int:job_id>/received-proposals/",
        JobProposalsView.as_view(),
        name="job-proposals",
    ),
    path(
        "proposals/<int:proposal_id>/action/",
        ProposalActionView.as_view(),
        name="proposal-action",
    ),
    path(
        "client/proposals-overview/",
        ClientProposalsOverviewView.as_view(),
        name="client-proposals-overview",
    ),
]
