from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# def get_progress(self):
#     total = self.subtasks.count()
#     completed = self.subtasks.filter(is_completed=True).count()

#     if total == 0:
#         return 100 if self.is_completed else 0

#     return int((completed / total) * 100)


# MIN_POINTS = 5

# def calculate_points(task, user):
#     base = task.estimated_hours * 10
#     rating_multiplier = 1 + (user.rating * 0.1)

#     points = base * rating_multiplier

#     return max(points, MIN_POINTS)

# Character -- ("Дябчик")
class Character(models.Model):
    name = models.CharField(max_length=255)
    experience = models.IntegerField(default=0)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} ({self.user})"
