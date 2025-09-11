from accounts.permissions import IsClient
from .models import Job
from .job_serializers import JobSerializer, JobResponseSerializer, JobUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from jobs import job_service
from drf_yasg.utils import swagger_auto_schema
from proposals.models import Proposal


class JobCreateView(APIView):

    permission_classes = [IsClient]

    @swagger_auto_schema(
        request_body=JobSerializer, responses={201: JobResponseSerializer}
    )
    def post(self, request):
        print(f"DEBUG: Request data: {request.data}")
        print(f"DEBUG: User: {request.user}")
        print(f"DEBUG: User authenticated: {request.user.is_authenticated}")
        if hasattr(request.user, "role"):
            print(f"DEBUG: User role: {request.user.role}")

        try:
            serializer = JobSerializer(data=request.data)
            print(f"DEBUG: Serializer created")

            serializer.is_valid(raise_exception=True)
            print(f"DEBUG: Serializer is valid")

            user = request.user
            validated_data = serializer.validated_data
            print(f"DEBUG: Validated data: {validated_data}")

            title = validated_data["title"]
            description = validated_data["description"]
            budget = validated_data["budget"]
            deadline = validated_data["deadline"]
            category = validated_data.get("category", "other")
            skills_required = validated_data.get("skills_required", [])
            experience_level = validated_data.get("experience_level", "intermediate")
            project_duration = validated_data.get("project_duration", "medium_term")
            job_type = validated_data.get("job_type", "fixed_price")
            print(f"DEBUG: About to call job_service.create_job")

            job = job_service.create_job(
                client_id=user.id,
                title=title,
                description=description,
                budget=budget,
                deadline=deadline,
                category=category,
                skills_required=skills_required,
                experience_level=experience_level,
                project_duration=project_duration,
                job_type=job_type,
            )
            print(f"DEBUG: Job created: {job}")

            response_data = JobResponseSerializer(job)
            print(f"DEBUG: Response data serialized")

            return Response(
                {"message": "Job was posted succesfully", "job": response_data.data},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            print(f"DEBUG: Exception occurred: {str(e)}")
            import traceback

            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MyJobView(APIView):

    def get(self, request):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Check if user is a client
        if not hasattr(request.user, "role") or request.user.role != "client":
            return Response(
                {"error": "Only clients can view their jobs"},
                status=status.HTTP_403_FORBIDDEN,
            )

        user = request.user
        try:
            jobs, error = job_service.get_job_byUserid(user.id)

            if error:
                return Response({"message": error}, status=status.HTTP_404_NOT_FOUND)

            response_data = JobResponseSerializer(jobs, many=True).data

            return Response({"jobs": response_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class JobView(APIView):
    def get(self, request):
        category = request.query_params.get("category", "all")

        try:
            jobs = job_service.get_jobs_by_category(category)
            response_data = JobResponseSerializer(jobs, many=True)

            return Response(
                {"jobs": response_data.data, "category": category},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class JobDetailView(APIView):
    def get(self, request, job_id):
        """Get job details - accessible by all authenticated users"""
        try:
            job = Job.objects.select_related("client").get(id=job_id)
            response_data = JobResponseSerializer(job).data
            
            # Check if this job has any accepted proposals
            has_accepted_proposal = Proposal.objects.filter(
                job=job, 
                status="accepted"
            ).exists()
            
            # Add the accepted proposal status to the response
            response_data['has_accepted_proposal'] = has_accepted_proposal
            
            return Response(response_data, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response(
                {"message": "Job not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, job_id):
        """Update job - only for clients who own the job"""
        if not hasattr(request.user, "role") or request.user.role != "client":
            return Response(
                {"message": "Only clients can update jobs"},
                status=status.HTTP_403_FORBIDDEN,
            )

        user = request.user
        serializer = JobUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            validated_data = serializer.validated_data
            job, error = job_service.updatejob_byid(
                job_id=job_id, clientid=user.id, **validated_data
            )

            if error == "UNAUTHORIZED":
                return Response({"message": error}, status=status.HTTP_403_FORBIDDEN)

            response_data = JobResponseSerializer(job)

            return Response(response_data.data, status=status.HTTP_200_OK)

        except Job.DoesNotExist:
            return Response(
                {"message": "Nothing found"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, job_id):
        user = request.user

        try:
            deleted, error = job_service.deletejob_byid(
                job_id=job_id, client_id=user.id
            )

            if error == "UNAUTHORIZED":
                return Response({"message": error}, status=status.HTTP_403_FORBIDDEN)

            if error == "NOT FOUND":
                return Response({"message": error}, status=status.HTTP_404_NOT_FOUND)

            return Response(
                {"message": "Deleted succesfully"}, status=status.HTTP_200_OK
            )

        except Job.DoesNotExist:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
