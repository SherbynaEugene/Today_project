from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Task, SubTask, Category
from django.views.decorators.http import require_POST
from django.db import models as db_models

MIN_POINTS = 5

def calculate_points(task, user):
    base = task.estimated_hours * 10
    rating_multiplier = 1 + (1 * 0.1) #it should be user ratinf * 0.1 or smth
    points = base * rating_multiplier
    return max(points, MIN_POINTS)

@login_required
def task_list(request):
    incomplete = Task.objects.filter(user=request.user, is_completed=False).order_by('order')
    completed = Task.objects.filter(user=request.user, is_completed=True).order_by('-created_at')
    categories = Category.objects.filter(user=request.user)
    print("INCOMPLETE:", incomplete)
    print("COMPLETED:", completed)
    return render(request, 'myapp/general_tasks.html', {
        'incomplete_tasks': incomplete,
        'completed_tasks': completed,
        'categories': categories,
    })


@login_required
def today_tasks(request):
    today = timezone.localdate()

    today_incomplete = Task.objects.filter(
        user=request.user,
        is_completed=False
    ).filter(
        db_models.Q(is_for_today=True) | db_models.Q(planned_date=today)
    ).order_by('order')

    other_incomplete = Task.objects.filter(
        user=request.user,
        is_for_today=False,
        is_completed=False,
        planned_date__isnull=True
    ).order_by('order')

    categories = Category.objects.filter(user=request.user)

    return render(request, 'myapp/user_desktop.html', {
        'today_tasks': today_incomplete,
        'other_tasks': other_incomplete,
        'categories': categories,
    })


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        estimated_hours = request.POST.get('duration', 1)
        planned_date = request.POST.get('planned_date') or None
        is_for_today = request.POST.get('is_for_today') == 'true'
        category_name = request.POST.get('category') or None
        deadline_time = request.POST.get('deadline_time', '12:00')

        category_id = None
        if category_name:
            # get_or_create шукає категорію, а якщо її немає створює
            category_id, created = Category.objects.get_or_create(
            name=category_name,
            defaults={'color': '#1f4d2b'} # Колір для нової категорії, якщо вона не знайдена
        )

        task = Task.objects.create(
            user=request.user,
            title=title,
            estimated_hours=estimated_hours,
            planned_date=planned_date,
            is_for_today=is_for_today,
            deadline_time=deadline_time,
            category=category_id,
        )
        return redirect('tasks:today_tasks')

    categories = Category.objects.filter(user=request.user)
    return render(request, 'tasks/add_task.html', {'categories': categories})

def move_to_today(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_for_today = True
    task.save()
    return redirect('tasks:today_tasks')

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_completed = True
    task.completed_at = timezone.now()
    task.save()

    # award points and coins
    points = calculate_points(task, request.user)
    request.user.total_points += int(points)
    request.user.coins += int(points)
    request.user.save()

    return redirect(request.META.get('HTTP_REFERER', 'myapp:user_desktop'))


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('tasks:task_list')

@login_required
@require_POST
def assign_task_to_date(request):
    task_id = request.POST.get('task_id_select')
    date_str = request.POST.get('date')
    redirect_url = request.POST.get('redirect', '/calendar/')
    confirm = request.POST.get('confirm')

    task = get_object_or_404(Task, id=task_id, user=request.user)

    # show confirmation if asignment has date
    if task.planned_date and str(task.planned_date) != date_str and not confirm:
        return render(request, 'myapp/confirm_reassign.html', {
            'task': task,
            'new_date': date_str,
            'redirect_url': redirect_url,
            'year': request.POST.get('year'),
            'month': request.POST.get('month'),
        })

    task.planned_date = date_str or None
    task.save()
    return redirect(redirect_url)


## LIMIT OF 3 TASKS PER DAY

# from django.utils import timezone
# from django.shortcuts import get_object_or_404, redirect
# from rating.services import reward_for_task_completion

# def complete_task(request, task_id):
#     task = get_object_or_404(Task, id=task_id, user=request.user)

#     if task.is_completed:
#         return redirect("tasks:today_tasks")

#     today = timezone.localdate()

#     completed_today = Task.objects.filter(
#         user=request.user,
#         is_completed=True,
#         completed_at__date=today
#     ).count()

#     if completed_today >= 3:
#         return redirect("tasks:today_tasks")  # або можна показати повідомлення

#     task.is_completed = True
#     task.completed_at = timezone.now()
#     task.save()

#     reward_for_task_completion(task)

#     return redirect("tasks:today_tasks")
