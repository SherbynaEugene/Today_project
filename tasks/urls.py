from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('today/', views.today_tasks, name='today_tasks'),
    path('add/', views.add_task, name='add_task'),
]