from .models import User
from django.contrib.auth import authenticate

#  helper function to get user by email

def get_user_byemail(email):
    
    try:
        user = User.objects.get(email=email)
        return user
    
    except User.DoesNotExist:
        return None
        

def signUp(username , email , password , role):
    
    if User.objects.filter(username=username).exists():
        return None , "INVALID USERNAME"
    
    if User.objects.filter(email=email).exists():
        return None, "INVALID EMAIL"
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        role=role
    )
    
    return user , None



def login(email , password):
    
    user = get_user_byemail(email=email)
    
    if not user:
        return None, 'INVALID EMAIL'
    
    the_user = authenticate(username=user.username , password=password)
    
    if not the_user:
        return None , 'INVALID PASSWORD'
    
    return the_user , None