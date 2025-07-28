from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker
from accounts.models import User
from jobs.models import Job
from datetime import date

fake = Faker()
class JobViewTests(APITestCase):

    def setUp(self):
        
        self.user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password="testpass123",
            role="client",
        )
        self.client.force_authenticate(user=self.user)
        self.deadline = date.today()

    def test_create_job(self):
        url = reverse("job-create")
        data = {
            "title": "Test Job",
            "description": "Test Description",
            "budget": 100,
            "deadline": self.deadline  
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Job posted successfully")

    def test_my_jobs_view_with_jobs(self):
        Job.objects.create(
            title="Job 1",
            description="Desc",
            budget=100,
            client=self.user,
            deadline=self.deadline,  
        )
        url = reverse("my-jobs")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_all_jobs(self):
        Job.objects.create(
            title="Job A",
            description="Desc A",
            budget=50,
            client=self.user,
            deadline=self.deadline,  
        )
        Job.objects.create(
            title="Job B",
            description="Desc B",
            budget=75,
            client=self.user,
            deadline=self.deadline,  
        )
        url = reverse("all-jobs")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 2)

    def test_update_job_authorized_user(self):
        job = Job.objects.create(
            title="Job C",
            description="Desc C",
            budget=90,
            client=self.user,
            deadline=self.deadline,  
        )
        url = reverse("job-detail", kwargs={"job_id": job.id})
        data = {"title": "Updated Job C"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Job updated successfully")