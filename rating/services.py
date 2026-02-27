from django.utils import timezone
from datetime import datetime
from django.db import transaction
from tasks.models import Task
from .models import UserRating, RatingHistory

BASE_POINTS = 100
MIN_MULTIPLIER = 0.5
MAX_MULTIPLIER = 2.0
LATE_PENALTY_MULTIPLIER = 0.3


def calculate_time_multiplier(task: Task):
    if not task.completed_at:
        return 0

    actual_seconds = (task.completed_at - task.created_at).total_seconds()

    if actual_seconds <= 0:
        return 1

    actual_hours = actual_seconds / 3600

    estimated_hours = task.estimated_hours if task.estimated_hours > 0 else 1


    planned_date = task.planned_date or timezone.localdate()
    # deadline_datetime = datetime.combine(planned_date, task.deadline_time)
    deadline_datetime = timezone.now()

    if task.completed_at > deadline_datetime:
        return LATE_PENALTY_MULTIPLIER

    ratio = estimated_hours / actual_hours

    return max(MIN_MULTIPLIER, min(ratio, MAX_MULTIPLIER))


@transaction.atomic
def reward_for_task_completion(task: Task):
    if not task.is_completed:
        return

    if RatingHistory.objects.filter(user=task.user, task=task).exists():
        return

    user_rating, _ = UserRating.objects.select_for_update().get_or_create(user=task.user)

    multiplier = calculate_time_multiplier(task)

    earned_points = BASE_POINTS * multiplier

    user_rating.total_points += earned_points
    user_rating.save()

    RatingHistory.objects.create(
        user=task.user,
        task=task,
        earned_points=earned_points,
        multiplier=multiplier,
        time_spent_hours=(task.completed_at - task.created_at).total_seconds() / 3600,
        estimated_hours=task.estimated_hours,
    )