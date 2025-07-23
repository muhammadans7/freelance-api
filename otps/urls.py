from django.urls import path
from .otp_views import VerifyOTPView

urlpatterns = [
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
]
