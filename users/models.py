from django.db import models
from django.contrib.auth.models import AbstractUser

# ---------- USER ----------
class User(AbstractUser):
    email = models.EmailField(unique=True)
    rating = models.IntegerField(default=1)
    total_points = models.IntegerField(default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
