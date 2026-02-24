from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import RatingHistory, UserRating


@login_required
def my_rating_view(request):
    rating, _ = UserRating.objects.get_or_create(user=request.user)

    return render(request, "rating/my_rating.html", {
        "rating": rating
    })


def leaderboard_view(request):
    top_users = UserRating.objects.select_related("user") \
        .order_by("-total_points")[:10]

    return render(request, "rating/leaderboard.html", {
        "top_users": top_users
    })