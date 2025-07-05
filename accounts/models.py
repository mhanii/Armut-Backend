from django.db import models
from django.contrib.auth.models import AbstractUser
from user_profile.models import User





class Verification(models.Model):
    user                        = models.OneToOneField(User, on_delete=models.CASCADE)
    code                        = models.CharField(max_length=6)
    is_verified                 = models.BooleanField(default=False)

    def __str__(self):
        return f"Verification for {self.user.username}"
