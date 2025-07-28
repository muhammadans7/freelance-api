from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .gig_views import GigsViewSet , MyGigView
router = DefaultRouter()
router.register(r"gigs", GigsViewSet, basename="gig")
urlpatterns = [
    path("", include(router.urls)),
    path("my-gigs/" , MyGigView.as_view() , name="my-gigs")
]
