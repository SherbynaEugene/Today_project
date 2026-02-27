
from django.shortcuts import render, redirect
from tasks.models import Task



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
def calendar(request):
    return render(request, 'myapp/calendar.html')
def interesting(request):
    return render(request, 'myapp/interesting.html')
def general_tasks(request):
    return render(request, 'myapp/general_tasks.html')
