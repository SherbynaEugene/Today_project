from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    rating = models.IntegerField(default=1)
    total_points = models.IntegerField(default=0)
    coins = models.IntegerField(default=100)  # added this for coin sysytem
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

class Character(models.Model):  # moved here from myapp/models.py
    name = models.CharField(max_length=255)
    experience = models.IntegerField(default=0)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} ({self.user})"
