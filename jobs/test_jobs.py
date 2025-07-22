

from django.test import TestCase
from accounts.models import User
from jobs.models import Job
from .job_service import (
    create_job,
    get_job_byUserid,
    get_all_jobs,
    updatejob_byid,
    deletejob_byid,
)
from datetime import date
# Create your tests here.



class JobServiceTest(TestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(
            username="client1",
            email="client@example.com",
            password="pass",
            role="client",
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@example.com", password="pass", role="client"
        )
        self.job = create_job(
            client_id=self.client_user.id,
            title="Website Design",
            description="Need a portfolio website",
            budget=500,
            deadline=date.today(),
        )

    def test_create_job_success(self):
        job = create_job(
            client_id=self.client_user.id,
            title="Mobile App",
            description="Need a mobile app",
            budget=1000,
            deadline=date.today(),
        )
        self.assertIsInstance(job, Job)
        self.assertEqual(job.title, "Mobile App")
        self.assertEqual(job.client, self.client_user)

    def test_get_job_by_userid_success(self):
        jobs, error = get_job_byUserid(self.client_user.id)
        self.assertIsNone(error)
        self.assertEqual(jobs.count(), 1)

    def test_get_job_by_userid_none(self):
        jobs, error = get_job_byUserid(self.other_user.id)
        self.assertIsNone(jobs)
        self.assertEqual(error, "You have not posted any job yet")

    def test_get_all_jobs(self):
        all_jobs = get_all_jobs()
        self.assertEqual(all_jobs.count(), 1)

    def test_update_job_by_owner_success(self):
        updated_job, error = updatejob_byid(
            job_id=self.job.id,
            clientid=self.client_user.id,
            title="Updated Title",
            budget=700,
        )
        self.assertIsNone(error)
        self.assertEqual(updated_job.title, "Updated Title")
        self.assertEqual(updated_job.budget, 700)

    def test_update_job_by_non_owner_fails(self):
        updated_job, error = updatejob_byid(
            job_id=self.job.id, clientid=self.other_user.id, title="Hacked!"
        )
        self.assertIsNone(updated_job)
        self.assertEqual(error, "UNAUTHORIZED")

    def test_delete_job_by_owner_success(self):
        deleted_count, error = deletejob_byid(self.job.id, self.client_user.id)
        self.assertIsNone(error)
        self.assertEqual(deleted_count, 1)

    def test_delete_job_by_non_owner_fails(self):
        deleted_count, error = deletejob_byid(self.job.id, self.other_user.id)
        self.assertIsNone(deleted_count)
        self.assertEqual(error, "UNAUTHORIZED")
