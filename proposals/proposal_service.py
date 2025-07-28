from .models import Proposal
from accounts.models import User
from jobs.models import Job

def get_job_byid(job_id):
    
    try:   
        job = Job.objects.get(id=job_id)
        return job
    
    except Job.DoesNotExist:
        return None

def create_Proposal(freelancer_id , job_id , cover_letter , proposed_rate=None):
    freelancer = User.objects.get(id=freelancer_id)
    job = get_job_byid(job_id=job_id)

    if not job:
        return None , "INVALID JOB ID"

    if Proposal.objects.filter(freelancer=freelancer , job=job).exists():
        return None, "You’ve already submitted a proposal for this job."
    
    proposal = Proposal(
        freelancer=freelancer,
        job=job,
        cover_letter=cover_letter,
        proposed_rate=proposed_rate
    ) 
    proposal.save()
    return proposal , None
    
    
