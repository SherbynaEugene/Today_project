from django.urls import path
from .views import my_rating_view, leaderboard_view
from . import views
app_name = 'rating'

urlpatterns = [
    path("my_rating/", my_rating_view, name="my_rating"),
    path("leaderboard/", leaderboard_view, name="leaderboard"),
    path("history/", views.rating_history, name="history"),
]
