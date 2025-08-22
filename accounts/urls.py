from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, LoginView, TokenCookieView, MeView

urlpatterns = [
    path("auth/signup/", RegisterView.as_view(), name="signup"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/cookie/", TokenCookieView.as_view(), name="token_cookie"),
    path("auth/me/", MeView.as_view(), name="me"),
]
