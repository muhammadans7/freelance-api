from accounts.permissions import IsFreelancer
from jobs.job_serializers import JobSerializer
from .models import Gig
from .gig_serializers import GigSerializer , GigResponseSerializer, UpdateGigSerializer
from gigs import gig_service
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class GigsViewSet(ModelViewSet):

    permission_classes = [IsFreelancer]

    serializer_class = GigSerializer
    queryset = Gig.objects.all()

    def create(self , request):

        user = request.user

        serializer = GigSerializer(data=request.data , context=self.get_serializer_context())

        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        title = validated_data["title"]
        description = validated_data["description"]
        price = validated_data["price"]
        delivery_time = validated_data["delivery_time"]

        try:

            gig = gig_service.add_gig(
                freelancer_id=user.id,
                title=title,
                description=description,
                price=price,
                delivery_time=delivery_time
            )

            return Response({"message" : "Gig was added successfully"} , status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error" : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self , request , pk=None):

        user = request.user

        try:

            gig, error = gig_service.get_gig_byid(user.id, pk)

            if error:
                return Response({"message": error}, status=status.HTTP_403_FORBIDDEN)

            serializer = GigResponseSerializer(
                gig, context=self.get_serializer_context()
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Gig.DoesNotExist:

            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, pk=None):

        serializer = UpdateGigSerializer(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)

        user = request.user

        try:

            validated_data = serializer.validated_data

            gig, error = gig_service.update_yourgig(pk, user.id, **validated_data)

            if error:
                return Response({"message": error}, status=status.HTTP_403_FORBIDDEN)

            response_data = GigResponseSerializer(gig)

            return Response(response_data.data, status=status.HTTP_200_OK)

        except Gig.DoesNotExist:

            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def destroy(self, request, pk=None):
        
        user = request.user
        
        try:
            
            deleted , error = gig_service.delete_gig_byid(pk , user.id)
            
            if error == "UNAUTHORIZED":
                return Response({"message" : error} , status=status.HTTP_403_FORBIDDEN)
            
            if error == "NOT FOUND":
                
                return Response({"message" : error} , status=status.HTTP_404_NOT_FOUND)
            
            
            return Response({"message" : "Successfully deleted"} , status=status.HTTP_200_OK)
        
        except Gig.DoesNotExist:
            
            return Response({"message" : "Not found"} , status=status.HTTP_404_NOT_FOUND)
            
        
        except Exception as e:
            
            return Response({"error" : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class MyGigView(APIView):
    
    permission_classes = [IsFreelancer]
    
    def get(self , request):
        
        user = request.user
        
        try:
            
            gigs , error =  gig_service.view_myown_gigs(user.id)
            
            if error:
                return Response({"message" : error} , status=status.HTTP_404_NOT_FOUND)
            
            response_data = GigResponseSerializer(gigs, many=True)
            
            return Response(
                {
                    "gigs" : response_data.data
                }
                , status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response({"error" : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)


