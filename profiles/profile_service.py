from accounts.models import User
from .models import Profile

def create_Profile(user_id , full_name , bio , hourly_rate=None): 
    user = User.objects.get(id=user_id)
    
    if (user.role == 'freelancer' or user.role == 'Freelancer') and (hourly_rate == None):
        return None , "NO HOURLY_RATE"
    
    if Profile.objects.filter(user=user).exists():
        return None , "PROFILE ALREADY EXISTS"
    
    profile = Profile(user=user, full_name=full_name , bio=bio , hourly_rate=hourly_rate)
   
    
    profile.save()
    
    return profile , None


def get_profile(user_id):
    
    user = User.objects.get(id=user_id)
    
   
    return Profile.objects.get(user=user)
    