from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task, SubTask, Category

MIN_POINTS = 5

def calculate_points(task, user):
    base = task.estimated_hours * 10
    rating_multiplier = 1 + (user.rating * 0.1)
    points = base * rating_multiplier
    return max(points, MIN_POINTS)


@login_required
def task_list(request):
    incomplete = Task.objects.filter(user=request.user, is_completed=False).order_by('order')
    completed = Task.objects.filter(user=request.user, is_completed=True).order_by('-created_at')
    categories = Category.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {
        'incomplete_tasks': incomplete,
        'completed_tasks': completed,
        'categories': categories,
    })


@login_required
def today_tasks(request):
    today_incomplete = Task.objects.filter(
        user=request.user, is_for_today=True, is_completed=False
    ).order_by('order')
    other_incomplete = Task.objects.filter(
        user=request.user, is_for_today=False, is_completed=False
    ).order_by('order')
    return render(request, 'tasks/today_tasks.html', {
        'today_tasks': today_incomplete,
        'other_tasks': other_incomplete,
    })


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        estimated_hours = request.POST.get('estimated_hours', 1)
        planned_date = request.POST.get('planned_date') or None
        is_for_today = request.POST.get('is_for_today') == 'on'
        category_id = request.POST.get('category') or None
        deadline_time = request.POST.get('deadline_time', '12:00')

        task = Task.objects.create(
            user=request.user,
            title=title,
            estimated_hours=estimated_hours,
            planned_date=planned_date,
            is_for_today=is_for_today,
            deadline_time=deadline_time,
            category_id=category_id,
        )
        return redirect('tasks:today_tasks')

    categories = Category.objects.filter(user=request.user)
    return render(request, 'tasks/add_task.html', {'categories': categories})


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_completed = True
    task.save()

    # Award points and coins
    points = calculate_points(task, request.user)
    request.user.total_points += int(points)
    request.user.coins += int(points)
    request.user.save()

    return redirect(request.META.get('HTTP_REFERER', 'tasks:today_tasks'))


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('tasks:task_list')
