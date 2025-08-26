from django.urls import path
from .proposal_view import ProposalCreateView, MyProposalsView, ProposalDetailView

urlpatterns = [
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
]
