from django.core.mail import send_mail
import pyotp
import qrcode
import base64
from io import BytesIO
from .models import TwoFactorAuth

def generate_2fa_secret_for_user(user):
    
    try:
        twofa = TwoFactorAuth.objects.get(user=user)
        
 
        
        if twofa.secret:
            raise Exception("2FA already set up for this user.")

       
        if twofa.secret:
            totp = pyotp.TOTP(twofa.secret)
            uri = totp.provisioning_uri(name=user.email, issuer_name="FreelancerAPI")
            return {
                "secret": twofa.secret,
                "otp_auth_url": uri
            }

    except TwoFactorAuth.DoesNotExist:
        pass
    
    
    secret = pyotp.random_base32()

    # creating 2fa in db or updating an existing one

    twofa , _ = TwoFactorAuth.objects.update_or_create(
        user=user,
        defaults={"secret" : secret , "is_enabled"  : False}
    )

    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=user.email , issuer_name="FreelancerAPI")


    return {
        "secret" : secret,
        "otp_auth_url" : uri
    }





def verify_2fa_token(user, token):
    twofa = TwoFactorAuth.objects.get(user=user)
    
    
    if twofa.is_enabled:
        return False
 
    secret = twofa.secret
    totp = pyotp.TOTP(secret)

    return totp.verify(token)
 


def generate_qr_code_base64(uri):
    
    img = qrcode.make(uri)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode()
    return f"data:image/png;base64,{img_base64}"




def send_2fa_enabled_email(user):
    subject = "2FA Enabled on Your Account"
    message = f"Hi {user.username},\n\nTwo-Factor Authentication (2FA) has been successfully enabled on your account."
    recipient_list = [user.email]

    send_mail(subject, message, None, recipient_list)
