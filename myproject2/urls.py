from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('user_desktop/', views.user_desktop, name='user_desktop'),
]
