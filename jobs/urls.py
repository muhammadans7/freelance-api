from django.urls import path
from .job_view import JobCreateView , MyJobView , JobView , JobDetailView


urlpatterns = [
    path("jobs/create/", JobCreateView.as_view(), name="job-create"),
    path("my-jobs/", MyJobView.as_view(), name="my-jobs"),
    path("all-jobs/", JobView.as_view(), name="all-jobs"),
    path("jobs/<int:job_id>/", JobDetailView.as_view(), name="job-detail"),
]
