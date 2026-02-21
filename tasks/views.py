from django.shortcuts import render
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def today_tasks(request):
    tasks = Task.objects.filter(is_for_today=True)
    return render(request, 'tasks/today_tasks.html', {'tasks': tasks})

def add_task(request):
    return render(request, 'tasks/add_task.html')