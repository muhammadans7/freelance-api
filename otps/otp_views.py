from rest_framework.views import APIView
from rest_framework import status

from accounts import serializers
from .otp_serializers import VerifyOTPSerializer
from .otp_service import verify_user_otp
from .models import OTPVerification
from rest_framework.response import Response

class VerifyOTPView(APIView):
    
    def post(self , request):
        
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)   
        validated_data = serializer.validated_data  
        try:    
            success , message = verify_user_otp(**validated_data)  
            if not success:
                return  Response({"message" : message} , status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message" : message} , status=status.HTTP_200_OK)
            
        except OTPVerification.DoesNotExist:
            return Response({"message" : "NO OTP FOUND"} , status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error" : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

