from django.urls import path
from .views import RegisterView , LoginView

urlpatterns = [
    path("auth/signup/", RegisterView.as_view(), name="signup"),
    path("auth/login/", LoginView.as_view(), name="login"),
]