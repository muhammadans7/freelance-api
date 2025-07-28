from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from twoFA.models import TwoFactorAuth
from .twoFA_services import (
    generate_2fa_secret_for_user,
    generate_qr_code_base64,
    verify_2fa_token,
    send_2fa_enabled_email
)
from .twoFA_serializers import Verify2FASerializer

class Start2FAView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request):
        user = request.user

        try:

            result =generate_2fa_secret_for_user(user)
            qr_base64 = generate_qr_code_base64(result["otp_auth_url"])

            return Response(
               
            {
                "message": "Scan this QR code with Google Authenticator",
                "qr_code_base64": qr_base64,
            },
            
            status=status.HTTP_200_OK,
        )

        except Exception as e:
            return Response({"error" : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Verify2FAView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self , request):
        
        serializer = Verify2FASerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data["token"]
        user = request.user
        
        try:
            
            if verify_2fa_token(user=user , token=token):
                
                twofa = TwoFactorAuth.objects.get(user=user)
                twofa.is_enabled = True
                twofa.save()
                send_2fa_enabled_email(user)
                
                return Response({"message" : "2FA verified successfully"} , status=status.HTTP_200_OK)
            
            else:
                return Response({"error" : "INVALID TOKEN OR 2FA IS ALREADY SETUP"} , status=status.HTTP_400_BAD_REQUEST)
            
        except TwoFactorAuth.DoesNotExist:
            return Response({"message" : "Not found"} , status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error" : str(e)} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)




