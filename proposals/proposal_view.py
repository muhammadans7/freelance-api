from accounts import serializers
from .models import Proposal
from accounts.permissions import IsFreelancer, IsClient
from .proposal_serializers import ProposalSerializer, ProposalResponseSerializer
from proposals import proposal_service
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from jobs.models import Job
from django.shortcuts import get_object_or_404


class ProposalCreateView(APIView):
    permission_classes = [IsFreelancer]

    def get(self, request, job_id):
        """Check if freelancer has already submitted a proposal for this job"""
        user = request.user
        try:
            proposal = Proposal.objects.get(freelancer=user, job_id=job_id)
            serializer = ProposalResponseSerializer(proposal)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Proposal.DoesNotExist:
            return Response(
                {"message": "No proposal found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, job_id):
        user = request.user
        serializer = ProposalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        cover_letter = validated_data["cover_letter"]
        proposed_rate = validated_data.get("proposed_rate")

        try:
            proposal, error = proposal_service.create_Proposal(
                freelancer_id=user.id,
                job_id=job_id,
                cover_letter=cover_letter,
                proposed_rate=proposed_rate,
            )

            if error == "INVALID JOB ID":
                return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)

            if error == "You've already submitted a proposal for this job.":
                return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)

            return Response(
                {"message": "Proposal was submitted succesfully"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MyProposalsView(APIView):
    permission_classes = [IsFreelancer]

    def get(self, request):
        """Get all proposals submitted by the current freelancer"""
        try:
            proposals = Proposal.objects.filter(freelancer=request.user).select_related(
                "job", "job__client"
            )
            serializer = ProposalResponseSerializer(proposals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProposalDetailView(APIView):
    permission_classes = [IsFreelancer]

    def get(self, request, proposal_id):
        """Get detailed information about a specific proposal"""
        try:
            proposal = Proposal.objects.select_related("job", "job__client").get(
                id=proposal_id, freelancer=request.user
            )
            serializer = ProposalResponseSerializer(proposal)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Proposal.DoesNotExist:
            return Response(
                {"message": "Proposal not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# === CLIENT VIEWS FOR MANAGING PROPOSALS ===


class JobProposalsView(APIView):
    """Client can view all proposals received for their specific job"""

    permission_classes = [IsClient]

    def get(self, request, job_id):
        """Get all proposals for a specific job (only job owner can access)"""
        try:
            # Ensure the job belongs to the current client
            job = get_object_or_404(Job, id=job_id, client=request.user)

            # Get all proposals for this job
            proposals = (
                Proposal.objects.filter(job=job)
                .select_related("freelancer")
                .prefetch_related("freelancer__profile")
                .order_by("-created_at")
            )

            serializer = ProposalResponseSerializer(proposals, many=True)

            # Add summary data
            proposal_summary = {
                "total_proposals": proposals.count(),
                "pending_proposals": proposals.filter(status="pending").count(),
                "accepted_proposals": proposals.filter(status="accepted").count(),
                "rejected_proposals": proposals.filter(status="rejected").count(),
            }

            return Response(
                {
                    "job": {
                        "id": job.id,
                        "title": job.title,
                        "budget": str(job.budget) if job.budget else None,
                        "job_type": job.job_type,
                    },
                    "summary": proposal_summary,
                    "proposals": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Job.DoesNotExist:
            return Response(
                {"message": "Job not found or you don't have permission to view it"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            # Add more detailed error logging
            import traceback

            print(f"Error in JobProposalsView: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProposalActionView(APIView):
    """Client can accept/reject proposals"""

    permission_classes = [IsClient]

    def patch(self, request, proposal_id):
        """Accept or reject a proposal"""
        try:
            # Get the proposal and ensure it belongs to client's job
            proposal = get_object_or_404(
                Proposal.objects.select_related("job", "freelancer"),
                id=proposal_id,
                job__client=request.user,
            )

            action = request.data.get("action")  # "accept" or "reject"

            if action not in ["accept", "reject"]:
                return Response(
                    {"message": "Invalid action. Use 'accept' or 'reject'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # If accepting, reject all other proposals for the same job
            if action == "accept":
                # Check if another proposal is already accepted for this job
                existing_accepted = (
                    Proposal.objects.filter(job=proposal.job, status="accepted")
                    .exclude(id=proposal.id)
                    .exists()
                )

                if existing_accepted:
                    return Response(
                        {
                            "message": "Another proposal has already been accepted for this job"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Accept this proposal
                proposal.status = "accepted"
                proposal.save()

                # Reject all other pending proposals for this job
                Proposal.objects.filter(job=proposal.job, status="pending").exclude(
                    id=proposal.id
                ).update(status="rejected")

                # TODO: Create project/contract here
                message = f"Proposal accepted successfully! Project will be created."

            else:  # reject
                if proposal.status == "accepted":
                    return Response(
                        {"message": "Cannot reject an already accepted proposal"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                proposal.status = "rejected"
                proposal.save()
                message = "Proposal rejected successfully"

            # Return updated proposal data
            serializer = ProposalResponseSerializer(proposal)
            return Response(
                {"message": message, "proposal": serializer.data},
                status=status.HTTP_200_OK,
            )

        except Proposal.DoesNotExist:
            return Response(
                {
                    "message": "Proposal not found or you don't have permission to modify it"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ClientProposalsOverviewView(APIView):
    """Client can see overview of all proposals across all their jobs"""

    permission_classes = [IsClient]

    def get(self, request):
        """Get overview of all proposals for client's jobs"""
        try:
            # Get all jobs posted by this client
            client_jobs = Job.objects.filter(client=request.user)

            # Get all proposals for these jobs
            proposals = (
                Proposal.objects.filter(job__in=client_jobs)
                .select_related("job", "freelancer", "freelancer__profile")
                .order_by("-created_at")
            )

            # Group proposals by job
            jobs_with_proposals = {}
            total_stats = {
                "total_proposals": 0,
                "pending_proposals": 0,
                "accepted_proposals": 0,
                "rejected_proposals": 0,
            }

            for proposal in proposals:
                job_id = proposal.job.id
                if job_id not in jobs_with_proposals:
                    jobs_with_proposals[job_id] = {
                        "job": {
                            "id": proposal.job.id,
                            "title": proposal.job.title,
                            "budget": (
                                str(proposal.job.budget)
                                if proposal.job.budget
                                else None
                            ),
                            "budget_type": proposal.job.budget_type,
                            "created_at": proposal.job.created_at.isoformat(),
                        },
                        "proposals": [],
                        "stats": {
                            "pending": 0,
                            "accepted": 0,
                            "rejected": 0,
                            "total": 0,
                        },
                    }

                # Add proposal to job
                proposal_data = ProposalResponseSerializer(proposal).data
                jobs_with_proposals[job_id]["proposals"].append(proposal_data)

                # Update stats
                jobs_with_proposals[job_id]["stats"][proposal.status] += 1
                jobs_with_proposals[job_id]["stats"]["total"] += 1

                # Update total stats
                total_stats["total_proposals"] += 1
                total_stats[f"{proposal.status}_proposals"] += 1

            return Response(
                {
                    "summary": total_stats,
                    "jobs_with_proposals": list(jobs_with_proposals.values()),
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
