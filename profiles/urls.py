from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet , MyProfileView

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profiles')

urlpatterns = [
    path('', include(router.urls)),
    path("my-profile/", MyProfileView.as_view(), name="my-profile"),
]
