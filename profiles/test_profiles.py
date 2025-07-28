from django.test import TestCase
from accounts.models import User
from .models import Profile
from profiles.profile_service import create_Profile, get_profile
from faker import Faker

fake = Faker()

class ProfileServiceTest(TestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(
            username= fake.user_name(),
            email= fake.email(),
            password= fake.password(),
            role="client",
        )
        self.freelancer_user = User.objects.create_user(
            
            username=fake.user_name(),
            email= fake.email(),
            password= fake.password(),
            role= "freelancer"
        )

    def test_create_profile_client_success(self):
        profile, error = create_Profile(
            user_id=self.client_user.id,
            full_name="Client User",
            bio="Just a client",
        )

        self.assertIsNotNone(profile)
        self.assertIsNone(error)
        self.assertEqual(profile.user, self.client_user)

    def test_create_profile_freelancer_requires_hourly_rate(self):
        profile, error = create_Profile(
            user_id=self.freelancer_user.id,
            full_name="Freelancer User",
            bio="Freelancer bio",
        )

        self.assertIsNone(profile)
        self.assertEqual(error, "NO HOURLY_RATE")

    def test_create_profile_freelancer_success(self):
        profile, error = create_Profile(
            user_id=self.freelancer_user.id,
            full_name="Freelancer User",
            bio="Freelancer bio",
            hourly_rate=50,
        )

        self.assertIsNotNone(profile)
        self.assertIsNone(error)
        self.assertEqual(profile.hourly_rate, 50)

    def test_create_duplicate_profile(self):
        create_Profile(
            user_id=self.client_user.id,
            full_name="Client",
            bio="First",
        )

        profile, error = create_Profile(
            user_id=self.client_user.id,
            full_name="Client again",
            bio="Second",
        )

        self.assertIsNone(profile)
        self.assertEqual(error, "PROFILE ALREADY EXISTS")

    def test_get_profile_success(self):
        created_profile, _ = create_Profile(
            user_id=self.client_user.id, full_name="Client", bio="Client bio"
        )

        retrieved_profile = get_profile(self.client_user.id)
        self.assertEqual(created_profile.id, retrieved_profile.id)
        self.assertEqual(retrieved_profile.user, self.client_user)
