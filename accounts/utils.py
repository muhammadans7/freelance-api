from rest_framework_simplejwt.tokens import RefreshToken

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh["email"] = user.email
    refresh["role"] = user.role
    return {
        "refresh" : str(refresh),
        "access" : str(refresh.access_token)
    }

ROLE_CHOICES = (
        ("user" , "User"),
        ("freelancer" , "Freelancer"),
        ("client" , "CLient")
)