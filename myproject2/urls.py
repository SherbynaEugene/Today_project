
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('users/', include('users.urls')),
    path('tasks/', include('tasks.urls')),
    path("rating/", include("rating.urls")),
    path('profile-shop/', include('profile_app.urls', namespace='profile_app')),
]
