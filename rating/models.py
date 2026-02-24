from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class UserRating(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="rating")
    total_points = models.FloatField(default=0)

    streak_days = models.IntegerField(default=0)
    last_completed_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | {self.total_points} pts"


class RatingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey("tasks.Task", on_delete=models.CASCADE)

    earned_points = models.FloatField()
    speed_bonus = models.FloatField()
    streak_multiplier = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "task")