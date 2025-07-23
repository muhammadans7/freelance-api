from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from faker import Faker
from accounts.models import User

fake = Faker()


class RegisterViewTests(APITestCase):

    def setUp(self):
        self.url = reverse("signup")  
        self.password = fake.password()

    def test_register_success(self):
        payload = {
            "username": fake.user_name(),
            "email": fake.email(),
            "password": self.password,
            "role": "freelancer",
        }

        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

    def test_register_existing_username(self):
      
        User.objects.create_user(
            username="sameuser",
            email=fake.email(),
            password=self.password,
            role="client",
        )

        payload = {
            "username": "sameuser",
            "email": fake.email(),
            "password": self.password,
            "role": "client",
        }

        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "User already exists")

    def test_register_existing_email(self):
        email = fake.email()
        User.objects.create_user(
            username=fake.user_name(),
            email=email,
            password=self.password,
            role="client",
        )

        payload = {
            "username": fake.user_name(),
            "email": email,
            "password": self.password,
            "role": "client",
        }

        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "User already exists")
