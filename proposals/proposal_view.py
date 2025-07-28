from accounts import serializers
from .models import Proposal
from accounts.permissions import IsFreelancer
from .proposal_serializers import ProposalSerializer , ProposalResponseSerializer
from proposals import  proposal_service
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class ProposalCreateView(APIView):
    permission_classes = [IsFreelancer]

    def post(self , request , job_id):
        user = request.user
        serializer = ProposalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        cover_letter = validated_data["cover_letter"]
        proposed_rate = validated_data.get("proposed_rate")

        try:
            proposal , error = proposal_service.create_Proposal(
                freelancer_id=user.id,
                job_id=job_id,
                cover_letter=cover_letter,
                proposed_rate=proposed_rate
            )

            if error == "INVALID JOB ID":
                return Response({"message" : error} , status=status.HTTP_400_BAD_REQUEST)

            if error == "You’ve already submitted a proposal for this job.":
                return Response({"message" : error} , status=status.HTTP_400_BAD_REQUEST)

            return Response({"message" : "Proposal was submitted succesfully"} , status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error" : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
    
