from django.shortcuts import render

def profile(request):
    return render(request, 'users/profile.html')

def register(request):
    return render(request, 'users/register.html')

def sign_in(request):
    return render(request, 'users/sign_in.html')