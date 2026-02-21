from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    planned_date = models.DateField(null=True, blank=True)
    is_for_today = models.BooleanField(default=False)
    deadline_time = models.TimeField(default="12:00")
    estimated_hours = models.FloatField(default=1)
    is_completed = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SubTask(models.Model):
    task = models.ForeignKey(Task, related_name="subtasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task.title} → {self.title}"