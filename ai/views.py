"""
AI Views for FreelanceHub Platform
API endpoints for AI-powered features
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .services import AIJobAssistant, AIProposalAssistant, AIPlatformAssistant
import json


class GenerateJobDescriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Generate improved job description using AI
        """
        try:
            data = request.data
            title = data.get("title", "")
            skills = data.get("skills", "")
            budget_range = data.get("budget_range", "")
            description_brief = data.get("description_brief", "")

            if not all([title, skills, description_brief]):
                return Response(
                    {
                        "error": "Missing required fields: title, skills, description_brief"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            result = AIJobAssistant.generate_job_description(
                title, skills, budget_range, description_brief
            )

            if result["success"]:
                return Response(
                    {
                        "generated_description": result["generated_description"],
                        "tokens_used": result["tokens_used"],
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": result["error"]},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GenerateProposalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Generate personalized proposal using AI
        """
        try:
            data = request.data
            job_description = data.get("job_description", "")
            freelancer_bio = (
                request.user.profile.bio if hasattr(request.user, "profile") else ""
            )
            freelancer_skills = (
                ", ".join([skill.name for skill in request.user.profile.skills.all()])
                if hasattr(request.user, "profile")
                else ""
            )

            if not job_description:
                return Response(
                    {"error": "Job description is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            result = AIProposalAssistant.generate_proposal(
                job_description, freelancer_bio, freelancer_skills
            )

            if result["success"]:
                return Response(
                    {
                        "generated_proposal": result["generated_proposal"],
                        "tokens_used": result["tokens_used"],
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": result["error"]},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PlatformAssistantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Get AI-powered platform assistance
        """
        try:
            data = request.data
            question = data.get("question", "")
            user_type = data.get("user_type", "freelancer")  

            if not question:
                return Response(
                    {"error": "Question is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            result = AIPlatformAssistant.get_platform_help(question, user_type)

            return Response(
                {
                    "response": result["response"],
                    "success": result["success"],
                    "tokens_used": result.get("tokens_used", 0),
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
