from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from myapp.models import Character
from .models import User


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Паролі не співпадають')
            return render(request, 'myapp/register.html', {
                'email': email,
                'username': username
            })

        if User.objects.filter(email=email).exists():
            messages.error(request, 'На цьому email вже є акаунт')
            return render(request, 'myapp/register.html', {
                'username': username
                # email зайнятий, нехай вводять інший
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        # creating automaticaly character for a new user
        Character.objects.create(name="Дябчик", user=user)

        login(request, user)
        return redirect('tasks:today_tasks')

    return render(request, 'myapp/register.html')


def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('tasks:today_tasks')
        else:
            messages.error(request, 'Неправильний email або пароль')
            return render(request, 'myapp/sign_in.html', {'email': email})

    return render(request, 'myapp/sign_in.html')


def sign_out(request):
    logout(request)
    return render(request, 'myapp/index.html')

@login_required
def profile(request):
    character = Character.objects.get(user=request.user)
    return render(request, 'myapp/profile.html', {
        'user': request.user,
        'character': character,
    })
