from .serializers import ProfileSerializer, ResponseSerializer
from .profile_service import create_Profile, get_profile
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from rest_framework.views import APIView


class ProfileViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def create(self, request):

        serializer = ProfileSerializer(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        user = request.user
        validated_data = serializer.validated_data
        full_name = validated_data["full_name"]
        bio = validated_data.get("bio")
        hourly_rate = validated_data.get("hourly_rate")

        new_fields = {
            "niche": validated_data.get("niche"),
            "skills": validated_data.get("skills", []),
            "experience_level": validated_data.get("experience_level"),
            "years_of_experience": validated_data.get("years_of_experience"),
            "languages": validated_data.get("languages", []),
            "preferred_project_types": validated_data.get(
                "preferred_project_types", []
            ),
            "minimum_project_budget": validated_data.get("minimum_project_budget"),
            "response_time": validated_data.get("response_time"),
        }

        try:
            profile, error = create_Profile(
                user_id=user.id,
                full_name=full_name,
                bio=bio,
                hourly_rate=hourly_rate,
                **new_fields
            )

            if error == "PROFILE ALREADY EXISTS" or error == "NO HOURLY_RATE":
                return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)

            return Response(
                {"message": "Profile was created successfully"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, pk=None, *args, **kwargs):

        partial = bool(kwargs.get("partial", False))
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response(
                {"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if profile.user != request.user:
            return Response(
                {"message": "Not allowed"}, status=status.HTTP_403_FORBIDDEN
            )
        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=partial,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        full_name = (
            validated_data.get("full_name") if "full_name" in validated_data else None
        )
        bio = validated_data.get("bio") if "bio" in validated_data else profile.bio
        hourly_rate_provided = "hourly_rate" in request.data
        hourly_rate = (
            validated_data.get("hourly_rate")
            if hourly_rate_provided
            else profile.hourly_rate
        )

        if "niche" in validated_data:
            profile.niche = validated_data.get("niche")
        if "skills" in validated_data:
            profile.skills = validated_data.get("skills", [])
        if "experience_level" in validated_data:
            profile.experience_level = validated_data.get("experience_level")
        if "years_of_experience" in validated_data:
            profile.years_of_experience = validated_data.get("years_of_experience")
        if "languages" in validated_data:
            profile.languages = validated_data.get("languages", [])
        if "preferred_project_types" in validated_data:
            profile.preferred_project_types = validated_data.get(
                "preferred_project_types", []
            )
        if "minimum_project_budget" in validated_data:
            profile.minimum_project_budget = validated_data.get(
                "minimum_project_budget"
            )
        if "response_time" in validated_data:
            profile.response_time = validated_data.get("response_time")

        user_role = getattr(profile.user, "role", "") or ""
        if user_role.lower() == "freelancer":
            if (not partial) or hourly_rate_provided:
                if hourly_rate is None:
                    return Response(
                        {"message": "NO HOURLY_RATE"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        if full_name is not None:
            profile.full_name = full_name
        profile.bio = bio
        if hourly_rate_provided:
            profile.hourly_rate = hourly_rate
        profile.save()

        return Response({"message": "Profile updated"}, status=status.HTTP_200_OK)


class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        try:
            profile = get_profile(user_id=user.id)
            response_data = ResponseSerializer(profile)
            return Response(response_data.data, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response(
                {"message": "You have not created your profile"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

