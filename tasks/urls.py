from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('today/', views.today_tasks, name='today_tasks'),
    path('add/', views.add_task, name='add_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('move-to-today/<int:task_id>/', views.move_to_today, name='move_to_today'),
    path('assign-to-date/', views.assign_task_to_date, name='assign_to_date'),
    path('unassign/<int:task_id>/', views.unassign_task, name='unassign_task'),
]
