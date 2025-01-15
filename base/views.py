from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'layout.html')

@login_required(login_url="login")
def chatapp(request):
    return render(request, 'pages/chat-app.html')

def logout_route(request):
    logout(request)
    return redirect("login")

def login_route(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username):
            messages.error(request, "Invalid username")
            return redirect("login")
        
        user = authenticate(username=username, password=password)
            
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('login')
        else:
            login(request, user)
            return redirect('/chat-app')
    return render(request, 'pages/login.html')

def register_route(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account successfully created!")
            return redirect('/login')
        else:
            messages.error(request, "Please correct the errors below.")
    
    else:
        form = CustomUserForm()

    return render(request, 'pages/register.html', {'form': form})