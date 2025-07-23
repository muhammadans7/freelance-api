from .models import OTPVerification
import secrets
from datetime import timedelta
from django.core.mail import send_mail
from django.utils import timezone
from accounts.models import User

# helper function to get user

def get_user_by_email(email):
    
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        return None


def generate_otp():
    return str(secrets.randbelow(899999) + 100000)



def send_otp_to_user(user):

    code = generate_otp()
    expiry = timezone.now() + timedelta(minutes=10)

    OTPVerification.objects.update_or_create(
        user=user,
        is_verified=False,
        defaults={"code" : code , "expires_at": expiry}
    )

    subject = "Your OTP Code"
    message = f"hello {user.username} , \n\n Your OTP is {code} , It expires in 10 minutes"

    send_mail(subject , message ,  None , [user.email])



def verify_user_otp(email , otp):
    
    user = get_user_by_email(email=email)
    
    if not User:
        return False , "User not found"
    
    otp_entry = OTPVerification.objects.get(user=user , is_verified=False)
    
    if otp_entry.is_expired():
        return False , "No OTP found"
    
    if otp_entry.code != otp:
        return False, "INCORRECT OTP"
    
    otp_entry.save()
    
    return True , "OTP verified Succesfully"
    


