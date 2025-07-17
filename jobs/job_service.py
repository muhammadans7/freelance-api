from http import client
from .models import Job
from accounts.models import User

def create_job(client_id , title , description , budget , deadline):
    
    client = User.objects.get(id=client_id)
    
    job = Job(client=client , title=title , description=description , budget=budget , deadline=deadline)
    job.save()
    
    return job


def get_job_byUserid(clientid):
    
    user = User.objects.get(id=clientid)
    
    jobs = Job.objects.filter(client=user)
    
    if not jobs.exists():
        return None , "You have not posted any job yet"
    
    return jobs , None



def get_all_jobs():
    return Job.objects.all()





def updatejob_byid(job_id , clientid, **kwargs):
    
    client = User.objects.get(id=clientid)
    
    job = Job.objects.get(id=job_id)
    
    if job.client != client:
        return None , "UNAUTHORIZED"
    
    
    for key , value in  kwargs.items():
        setattr(job , key , value)
        
    job.save()
    return job , None


def deletejob_byid(job_id , client_id):
    
    client = User.objects.get(id=client_id)
    
    job = Job.objects.get(id=job_id)
    
    if job.client != client:
        return None , "UNAUTHORIZED"
    
    deleted  , _ = Job.objects.filter(id=job_id).delete()
    
    if deleted == 0:
        return None , "NOT FOUND"
    
    return deleted , None