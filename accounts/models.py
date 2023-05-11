from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    This class extends the default User model with additional fields
    """
    # Add additional fields for the user profile
    home_address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.PointField(null=True, blank=True)

    def __str__(self):
        return self.username
