from django.shortcuts import render

def index(request):
    return render(request, 'myapp/index.html')
def register(request):
    return render(request, 'myapp/register.html')
def sign_in(request):
    return render(request, 'myapp/sign_in.html')
def profile(request):
    return render(request, 'myapp/profile.html')
