from django.db import models
from accounts.models import User

class TwoFactorAuth(models.Model):
    
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name="two_factor_auth")
    secret = models.CharField(max_length=32)
    is_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} -2FA {'enabled' if self.is_enabled else 'disabled'}"
        