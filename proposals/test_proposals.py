from django.test import Client, TestCase
from accounts.models import User
from jobs.models import Job
from jobs.job_service import create_job
from .models import Proposal
from .proposal_service import (
    
    create_Proposal,
)
from datetime import date
class ProposalServiceTest(TestCase):
    
    def setUp(self):
        self.freelancer_user = User.objects.create_user(
            username="freelancer1",
            email="freelancer@example.com",
            password="abc123",
            role="freelancer"
        )    
        self.client_user = User.objects.create_user(
            username="client1" , email="client@example.com" , password="pass" , role="client"
        )  
        self.job = create_job(
            client_id=self.client_user.id,
            title="Website Deisgn",
            description="Need a portfolio website",
            budget=500,
            deadline=date.today()
        )
        
    def test_create_proposal_success(self):
        proposal , error = create_Proposal(
            freelancer_id=self.freelancer_user.id,
            job_id=self.job.id,
            cover_letter="I have experience in web dev",
            proposed_rate=250
        )  
        self.assertIsNotNone(proposal)
        self.assertIsNone(error)
        self.assertEqual(proposal.job, self.job)
        self.assertEqual(proposal.freelancer, self.freelancer_user)