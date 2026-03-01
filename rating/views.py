from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import RatingHistory, UserRating

@login_required
def my_rating_view(request):
    rating, _ = UserRating.objects.get_or_create(user=request.user)

    history = RatingHistory.objects.filter(
        user=request.user
    ).select_related("task").order_by("-created_at")[:20]

    return render(request, "rating/my_rating.html", {
        "rating": rating,
        "history": history,
    })


def leaderboard_view(request):
    top_users = UserRating.objects.select_related("user") \
        .order_by("-total_points")[:10]

    return render(request, "rating/leaderboard.html", {
        "top_users": top_users
    })



@login_required
def rating_history(request):
    history = RatingHistory.objects.filter(
        user=request.user
    ).select_related("task").order_by("-created_at")

    return render(request, "rating/history.html", {
        "history": history
    })
