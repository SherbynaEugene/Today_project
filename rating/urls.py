from django.urls import path
from .views import my_rating_view, leaderboard_view

app_name = 'rating'

urlpatterns = [
    path("my_rating/", my_rating_view, name="my_rating"),
    path("leaderboard/", leaderboard_view, name="leaderboard"),
]
