from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tasks.models import Task
from datetime import date
import calendar as cal

def index(request):
    return render(request, 'myapp/index.html')

def register(request):
    return render(request, 'myapp/register.html')

def sign_in(request):
    return render(request, 'myapp/sign_in.html')

def profile(request):
    return redirect('/profile-shop/')

def user_desktop(request):
    tasks = Task.objects.all()
    return render(request, 'myapp/user_desktop.html', {'tasks': tasks})

def interesting(request):
    return render(request, 'myapp/interesting.html')

def general_tasks(request):
    return render(request, 'myapp/general_tasks.html')

@login_required
def calendar(request):
    today = date.today()

    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    selected_date_str = request.GET.get('date')
    selected_date = None
    day_tasks = []

    if selected_date_str:
        try:
            selected_date = date.fromisoformat(selected_date_str)
            day_tasks = Task.objects.filter(
                user=request.user,
                planned_date=selected_date,
                is_completed=False
            )
        except ValueError:
            pass

    cal_matrix = cal.monthcalendar(year, month)
    all_tasks = Task.objects.filter(user=request.user, is_completed=False) #all uncomplete tasks for sidebar

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    MONTHS = ['','СІЧЕНЬ','ЛЮТИЙ','БЕРЕЗЕНЬ','КВІТЕНЬ','ТРАВЕНЬ','ЧЕРВЕНЬ',
                 'ЛИПЕНЬ','СЕРПЕНЬ','ВЕРЕСЕНЬ','ЖОВТЕНЬ','ЛИСТОПАД','ГРУДЕНЬ']

    return render(request, 'myapp/calendar.html', {
        'cal_matrix': cal_matrix,
        'year': year,
        'month': month,
        'month_name': MONTHS[month],
        'selected_date': selected_date,
        'selected_date_str': selected_date_str,
        'day_tasks': day_tasks,
        'all_tasks': all_tasks,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'today': today,
        'day_names': ['ПН','ВТ','СР','ЧТ','ПТ','СБ','НД'],
    })
