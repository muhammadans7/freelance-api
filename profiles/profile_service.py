from accounts.models import User
from .models import Profile


def create_Profile(user_id, full_name, bio, hourly_rate=None, **kwargs):
    user = User.objects.get(id=user_id)

    if (user.role == "freelancer" or user.role == "Freelancer") and (
        hourly_rate == None
    ):
        return None, "NO HOURLY_RATE"

    if Profile.objects.filter(user=user).exists():
        return None, "PROFILE ALREADY EXISTS"

    niche = kwargs.get("niche")
    skills = kwargs.get("skills", [])
    experience_level = kwargs.get("experience_level")
    years_of_experience = kwargs.get("years_of_experience")
    languages = kwargs.get("languages", [])
    preferred_project_types = kwargs.get("preferred_project_types", [])
    minimum_project_budget = kwargs.get("minimum_project_budget")
    response_time = kwargs.get("response_time")

    profile = Profile(
        user=user,
        full_name=full_name,
        bio=bio,
        hourly_rate=hourly_rate,
        niche=niche,
        skills=skills,
        experience_level=experience_level,
        years_of_experience=years_of_experience,
        languages=languages,
        preferred_project_types=preferred_project_types,
        minimum_project_budget=minimum_project_budget,
        response_time=response_time,
    )

    profile.save()

    return profile, None


def get_profile(user_id):

    user = User.objects.get(id=user_id)

    return Profile.objects.get(user=user)
