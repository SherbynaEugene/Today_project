
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'myapp/index.html')
def register(request):
    return render(request, 'myapp/register.html')
def sign_in(request):
    return render(request, 'myapp/sign_in.html')
def profile(request):
    return redirect('/profile-shop/')
def user_desktop(request):
    return render(request, 'myapp/user_desktop.html')
