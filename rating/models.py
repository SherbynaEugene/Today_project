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

    earned_points = models.FloatField(default=0)
    multiplier = models.FloatField(default=1)
    time_spent_hours = models.FloatField(default=0)
    estimated_hours = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def time_spent_formatted(self):
        total_minutes = int(self.time_spent_hours * 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours} год {minutes} хв"

    class Meta:
        unique_together = ("user", "task")



