from django.urls import path
from .proposal_view import ProposalCreateView

urlpatterns = [
    
    path("jobs/<int:job_id>/proposals/" , ProposalCreateView.as_view() , name="create-proposal")
    
    # path(
    #     "jobs/<int:job_id>/proposals/",
    #     ProposalCreateView.as_view(),
    #     name="create-proposal",
    # ),
]
