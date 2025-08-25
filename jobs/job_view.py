from accounts.permissions import IsClient
from .models import Job
from .job_serializers import JobSerializer, JobResponseSerializer, JobUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from jobs import job_service
from drf_yasg.utils import swagger_auto_schema


class JobCreateView(APIView):

    permission_classes = [IsClient]

    @swagger_auto_schema(
        request_body=JobSerializer, responses={201: JobResponseSerializer}
    )
    def post(self, request):

        serializer = JobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        validated_data = serializer.validated_data
        title = validated_data["title"]
        description = validated_data["description"]
        budget = validated_data["budget"]
        deadline = validated_data["deadline"]
        category = validated_data.get("category", "other")

        try:
            job = job_service.create_job(
                client_id=user.id,
                title=title,
                description=description,
                budget=budget,
                deadline=deadline,
                category=category,
            )

            response_data = JobResponseSerializer(job)

            return Response(
                {"message": "Job was posted succesfully", "job": response_data.data},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MyJobView(APIView):

    permission_classes = [IsClient]

    def get(self, request):
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
    permission_classes = [IsClient]

    def put(self, request, job_id):

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
