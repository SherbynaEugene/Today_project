from datetime import time, datetime
from django.utils import timezone
from tasks.models import Task
from .models import UserRating, RatingHistory
from django.db import transaction

BASE_POINTS = 50

def is_task_completed_on_time(task: Task) -> bool:

    if not task.completed_at or not task.planned_date:
        return False

    end_of_day = time(hour=23, minute=59)
    deadline_naive = datetime.combine(task.planned_date, end_of_day)
    deadline = timezone.make_aware(deadline_naive)

    return task.completed_at <= deadline


@transaction.atomic
def reward_for_task_completion(task: Task):

    if not task.is_completed:
        return

    if RatingHistory.objects.filter(user=task.user, task=task).exists():
        return

    user_rating, _ = UserRating.objects.select_for_update().get_or_create(user=task.user)


    earned_points = BASE_POINTS * task.estimated_hours if is_task_completed_on_time(task) else 0

    if earned_points > 0:
        user_rating.total_points += earned_points
        user_rating.save()

    RatingHistory.objects.create(
        user=task.user,
        task=task,
        earned_points=earned_points,
        multiplier=1 if earned_points > 0 else 0,
        time_spent_hours=(task.completed_at - task.created_at).total_seconds() / 3600,
        estimated_hours=task.estimated_hours,
    )

    if earned_points > 0:
        user_rating.update_streak()
