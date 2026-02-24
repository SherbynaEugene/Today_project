from django.utils import timezone
from datetime import datetime, timedelta
from django.db import transaction
from tasks.models import Task
from .models import UserRating, RatingHistory

# Constants
BASE_POINTS = 100
MAX_STREAK_BONUS = 0.25
MIN_SPEED_RATIO = 0.5

def calculate_speed_bonus(task: Task):
    now = timezone.now()

    if not task.is_for_today:
        return 1

    today = timezone.localdate()
    deadline_datetime = datetime.combine(today, task.deadline_time)
    deadline_datetime = timezone.make_aware(deadline_datetime)

    total_time = (deadline_datetime - task.created_at).total_seconds()
    time_passed = (now - task.created_at).total_seconds()

    if total_time <= 0:
        return 1

    ratio = 1 - (time_passed / total_time)
    return max(ratio, MIN_SPEED_RATIO)

def update_streak(user_rating: UserRating):

    today = timezone.localdate()

    if user_rating.last_completed_date == today:
        return

    if user_rating.last_completed_date == today - timedelta(days=1):
        user_rating.streak_days += 1
    else:
        user_rating.streak_days = 1

    user_rating.last_completed_date = today

def calculate_streak_multiplier(streak_days: int):
    bonus = min(streak_days * 0.01, MAX_STREAK_BONUS)
    return 1 + bonus

@transaction.atomic
def reward_for_task_completion(task: Task):
    if not task.is_completed:
        return
    if RatingHistory.objects.filter(user=task.user, task=task).exists():
        return

    user_rating, _ = UserRating.objects.select_for_update().get_or_create(user=task.user)

    speed_bonus = calculate_speed_bonus(task)
    update_streak(user_rating)
    streak_multiplier = calculate_streak_multiplier(user_rating.streak_days)

    earned_points = BASE_POINTS * speed_bonus * streak_multiplier
    user_rating.total_points += earned_points
    user_rating.save()

    RatingHistory.objects.create(
        user=task.user,
        task=task,
        earned_points=earned_points,
        speed_bonus=speed_bonus,
        streak_multiplier=streak_multiplier,
    )