from .models import Gig
from accounts.models import User

def add_gig(freelancer_id , title , description , price , delivery_time):
    
    freelancer = User.objects.get(id=freelancer_id)
    
    gig = Gig(freelancer=freelancer , title=title , description=description , price=price , delivery_time=delivery_time)
    gig.save()
    
    return gig

def view_myown_gigs(freelancer_id):
    
    freelancer = User.objects.get(id=freelancer_id)
    
    gigs = Gig.objects.filter(freelancer=freelancer)
    
    if not gigs.exists():
        return None , "You have not added any gig yet"
    
    return gigs , None

def get_all_gigs_added():
    return Gig.objects.all()

def get_gig_byid(freelancer_id , gig_id):
    
    freelancer = User.objects.get(id=freelancer_id)
    
    gig = Gig.objects.get(id=gig_id)
    
    if gig.freelancer != freelancer:
        return None , "UNAUTHORIZED"
    
    return gig , None

def update_yourgig(gig_id , freelancer_id , **kwargs):  
    freelancer = User.objects.get(id=freelancer_id)
    
    gig = Gig.objects.get(id=gig_id)
    
    if gig.freelancer != freelancer:
        return None , "UNAUTHORIZED"
    
    for key , value in kwargs.items():
        setattr(gig , key , value)
        
    gig.save()
        
    return gig , None

def delete_gig_byid(gig_id , freelancer_id):
    freelancer = User.objects.get(id=freelancer_id)
    
    gig = Gig.objects.get(id=gig_id)
    
    if gig.freelancer != freelancer:
        return None , "UNAUTHORIZED"
    
    
    deleted , _ =  Gig.objects.filter(id=gig_id).delete()
    
    if deleted == 0:
        return None , "NOT FOUND"
    
    return deleted , None


