from .twoFA_views import Start2FAView , Verify2FAView
from django.urls import path

urlpatterns = [
    path("2fa/start/", Start2FAView.as_view(), name="start-2fa"),
    path("2fa/verify/", Verify2FAView.as_view(), name="verify-2fa"),
]
