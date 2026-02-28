from datetime import datetime, time
from django.utils import timezone
from tasks.models import Task
from .models import UserRating, RatingHistory
from django.db import transaction

BASE_POINTS = 100
MIN_MULTIPLIER = 0.5
MAX_MULTIPLIER = 2.0


def calculate_time_multiplier(task: Task):

    if not task.completed_at:
        return 0

    # Якщо немає дати або часу — не даємо рейтинг
    if not task.planned_date:
        return 0

    def estimated_hours_to_time(estimated_hours: float) -> time:
        hours = int(estimated_hours)
        minutes = round((estimated_hours - hours) * 60)
        if minutes == 60:
            hours += 1
            minutes = 0
        hours = min(hours, 23)
        return time(hour=hours, minute=minutes)

    deadline_time = estimated_hours_to_time(task.estimated_hours)

    deadline_naive = datetime.combine(
        task.planned_date,
        deadline_time
    )

    deadline_datetime = timezone.make_aware(deadline_naive)
    print("DEADLINE:", deadline_datetime)

    if task.completed_at > deadline_datetime:
        return 0

    actual_seconds = (task.completed_at - task.created_at).total_seconds()

    if actual_seconds <= 0:
        return 1

    actual_hours = actual_seconds / 3600
    estimated_hours = task.estimated_hours if task.estimated_hours > 0 else 1

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

    # Якщо earned_points = 0 — просто не додаємо до total_points
    if earned_points > 0:
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
