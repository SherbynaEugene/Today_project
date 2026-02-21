from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('sign_in/', views.sign_in, name='sign_in'),
]
