from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from faker import Faker
from accounts.models import User
from .models import Profile
from rest_framework_simplejwt.tokens import RefreshToken

fake = Faker()


def get_auth_client(user):
    token = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token.access_token)}")
    return client


class ProfileViewTests(APITestCase):

    def setUp(self):
        
        self.user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password(),
            role="freelancer",
        )
        self.client = get_auth_client(self.user)

    def test_create_profile_success(self):
        
        url = reverse("profile-list") 
        data = {"full_name": fake.name(), "bio": fake.text(), "hourly_rate": 40}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "Profile was created successfully")

    def test_create_profile_without_hourly_rate(self):
        
        url = reverse("profile-list")
        data = {"full_name": fake.name(), "bio": fake.text()}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "NO HOURLY_RATE")

    def test_create_profile_already_exists(self):
      
        Profile.objects.create(
            user=self.user, full_name="Already Exists", hourly_rate=50
        )

        url = reverse("profile-list")
        data = {"full_name": fake.name(), "bio": fake.text(), "hourly_rate": 70}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "PROFILE ALREADY EXISTS")

    def test_get_my_profile_success(self):
        
        profile = Profile.objects.create(
            user=self.user, full_name="Test User", bio="bio", hourly_rate=60
        )
        url = reverse("my-profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["full_name"], "Test User")

    def test_get_profile_does_not_exist(self):
        url = reverse("my-profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["message"], "You have not created your profile")
