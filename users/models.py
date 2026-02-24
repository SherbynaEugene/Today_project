from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    total_points = models.IntegerField(default=0)
    coins = models.IntegerField(default=100)  # added this for coin sysytem
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
