import os
from .utils import get_token_for_user
from .serializers import RegisterSerializer, LoginSerializer, UserResponseSerializer
from .services import signup, login
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=RegisterSerializer, responses={201: UserResponseSerializer}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            user, error = signup(**validated_data)

            if error == "INVALID USERNAME" or error == "INVALID EMAIL":
                return Response(
                    {"message": "User already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            response_data = UserResponseSerializer(user)
            return Response(
                {"message": "EMAIL SENT TO YOU WITH OTP PLZ VERIFY"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer, responses={201: UserResponseSerializer}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        try:
            user, error = login(**validated_data)

            if error == "INVALID EMAIL" or error == "INVALID PASSWORD":
                return Response(
                    {"message": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            tokens = get_token_for_user(user)
            response_data = UserResponseSerializer(user)

            return Response(
                {"user": response_data.data, "tokens": tokens},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TokenCookieView(APIView):
    """Helper endpoint: authenticate user, set HttpOnly refresh cookie and return access token."""

    @swagger_auto_schema(
        request_body=LoginSerializer, responses={200: UserResponseSerializer}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            user, error = login(**validated_data)
            if error == "INVALID EMAIL" or error == "INVALID PASSWORD":
                return Response(
                    {"message": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            tokens = get_token_for_user(user)

            # Build response with access token in body and refresh token in HttpOnly cookie
            response = Response(
                {"access": tokens.get("access")}, status=status.HTTP_200_OK
            )

            # Cookie settings: secure if env says so (for production behind HTTPS)
            cookie_secure = os.getenv("COOKIE_SECURE", "False").lower() in (
                "1",
                "true",
                "yes",
            )
            cookie_samesite = os.getenv("COOKIE_SAMESITE", "Lax")
            cookie_domain = os.getenv("COOKIE_DOMAIN", None)

            # Set refresh token as HttpOnly cookie
            response.set_cookie(
                key="refresh",
                value=tokens.get("refresh"),
                httponly=True,
                secure=cookie_secure,
                samesite=cookie_samesite,
                domain=cookie_domain,
                path="/",
            )

            return response

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
