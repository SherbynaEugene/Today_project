from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#000000')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    planned_date = models.DateField(null=True, blank=True)
    is_for_today = models.BooleanField(default=False)
    deadline_time = models.TimeField(default="12:00")
    estimated_hours = models.FloatField(default=1)
    is_completed = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_progress(self):  # i moved it here from myapp/models.py. if all agreed i`ll delete it there later
        total = self.subtasks.count()
        completed = self.subtasks.filter(is_completed=True).count()
        if total == 0:
            return 100 if self.is_completed else 0
        return int((completed / total) * 100)

class SubTask(models.Model):
    task = models.ForeignKey(Task, related_name="subtasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task.title} → {self.title}"
