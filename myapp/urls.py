from django.urls import path
from .views import index, register, sign_in, profile, user_desktop

app_name = "myapp"

urlpatterns = [
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('register/', register, name='register'),
    path('sign_in/', sign_in, name='sign_in'),
    path('profile/', profile, name='profile'),
    path('user_desktop/', user_desktop, name='user_desktop'),
]