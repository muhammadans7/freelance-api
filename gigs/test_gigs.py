from django.test import TestCase
from accounts.models import User
from .models import Gig

from .gig_service import (
    add_gig,
    view_myown_gigs,
)
class GigServiceTest(TestCase):
    
    def setUp(self):
        self.freelancer_user = User.objects.create_user(
            username="freelancer1",
            email="freelancer@example.com",
            password="pass",
            role="freelancer"
        )
        
        self.other_user = User.objects.create_user(
            username="other" , email="other@example.com" , password="pass", role="client"
        )
        
        
        self.gig = add_gig(
            freelancer_id=self.freelancer_user.id,
            title="portfolio in html css",
            description="portflio with react + tailwind",
            price=500,
            delivery_time=15
            
        )
    def test_create_gig_success(self):
        
        gig = add_gig(
            freelancer_id=self.freelancer_user.id,
            title="mobile app",
            description="mobile app in flutter",
            price=1000,
            delivery_time=15
        )
        
        self.assertIsInstance(gig , Gig)
        self.assertEqual(gig.title , "mobile app")
        self.assertEqual(gig.freelancer , self.freelancer_user)
        
    def test_view_myown_gigs(self):
        
        gigs , error = view_myown_gigs(self.freelancer_user.id)
        
        self.assertIsNone(error)
        self.assertEqual(gigs[0].title , "portfolio in html css")
        self.assertEqual(gigs[0].freelancer , self.freelancer_user)