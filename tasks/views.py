from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Task, SubTask, Category
from django.views.decorators.http import require_POST
from django.db import models as db_models
from datetime import datetime

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
    ).order_by('order')

    categories = Category.objects.filter(user=request.user)

    return render(request, 'myapp/user_desktop.html', {
        'today_tasks': today_incomplete,
        'other_tasks': other_incomplete,
        'categories': categories,
        'today': today,
    })

@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        estimated_hours = request.POST.get('duration', 1)
        is_for_today = request.POST.get('is_for_today') == 'true'

        planned_date = request.POST.get('planned_date')
        if is_for_today:
            planned_date = timezone.localdate()
        else:
            planned_date = None
        category_name = request.POST.get('category') or None
        deadline_time = request.POST.get('deadline_time', '23:00')


        # Перевірка: якщо завдання на сьогодні після 12:00
        now = timezone.localtime()
        if planned_date == timezone.localdate() and now.hour >= 12:
            messages.error(request, "Після 12:00 завдання на сьогодні створювати не можна.")
            return redirect(request.META.get('HTTP_REFERER', 'myapp:user_desktop'))
        category_id = None
        if category_name:
            category_id, created = Category.objects.get_or_create(
            user=request.user,
            name=category_name,
            defaults={'color': '#1f4d2b'}
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


@login_required
def move_to_today(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    now = timezone.localtime()

    if now.hour >= 12:
        messages.error(request, "Після 12:00 не можна переносити завдання на сьогодні.")
        return redirect(request.META.get('HTTP_REFERER', 'tasks:today_tasks'))

    task.is_for_today = True
    task.planned_date = timezone.localdate()
    task.save()

    messages.success(request, "Завдання успішно перенесено на сьогодні.")
    return redirect('tasks:today_tasks')


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    current_time = timezone.localtime().time()


    if not task.is_completed:
        task.is_completed = True
        task.completed_at = timezone.now()
        task.save()

        points = calculate_points(task, request.user)
        request.user.total_points += int(points)
        request.user.coins += int(points)
        request.user.save()

    return redirect(request.META.get('HTTP_REFERER', 'myapp:user_desktop'))

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect(request.META.get('HTTP_REFERER', 'tasks:task_list'))


@login_required
@require_POST
def assign_task_to_date(request):
    task_id = request.POST.get('task_id_select')
    date_str = request.POST.get('date')
    redirect_url = request.POST.get('redirect', '/calendar/')
    confirm = request.POST.get('confirm')

    task = get_object_or_404(Task, id=task_id, user=request.user)

    if date_str:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        now = timezone.localtime()

        if selected_date == timezone.localdate() and now.hour >= 12:
            messages.error(request, "Після 12:00 не можна додавати завдання на сьогодні.")
            return redirect(request.META.get('HTTP_REFERER', 'myapp:user_desktop'))

    # show confirmation if assignment has date
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

@login_required
def unassign_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.planned_date = None
    task.save()
    return redirect(request.META.get('HTTP_REFERER', '/calendar/'))
