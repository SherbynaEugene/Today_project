from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks.models import Task
from rating.models import UserRating
from rating.services import BASE_POINTS


class Command(BaseCommand):
    help = "Check daily tasks and apply rating penalty if needed"

    def handle(self, *args, **kwargs):
        today = timezone.localdate()

        ratings = UserRating.objects.select_related("user")

        for user_rating in ratings:
            user = user_rating.user

            if user_rating.last_penalty_date == today:
                continue

            today_tasks = Task.objects.filter(
                user=user,
                planned_date=today
            )

            if not today_tasks.exists():
                continue

            if today_tasks.filter(is_completed=True).exists():
                continue

            max_possible_points = sum(
                BASE_POINTS * float(task.estimated_hours) * user_rating.current_streak
                for task in today_tasks
            )

            user_rating.total_points -= max_possible_points

            if user_rating.total_points < 0:
                user_rating.total_points = 0

            user_rating.last_penalty_date = today
            user_rating.save()

        self.stdout.write(self.style.SUCCESS("Daily rating check completed"))
