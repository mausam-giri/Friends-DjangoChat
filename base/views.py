from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Messages
from django.http import JsonResponse
from django.db import models

def index(request):
    users = None
    if request.user.is_authenticated:
        users = User.objects.exclude(id=request.user.id)
    return render(request, 'layout.html', {'users': users})

@login_required(login_url="login")
def chatapp(request, username=None):
    users = User.objects.exclude(id=request.user.id) if request.user.is_authenticated else None
    friend = None

    if username:
        friend = get_object_or_404(User, username=username)

    return render(request, 'pages/chat-app.html', {'users': users, 'friend': friend})

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
            return redirect('chat-app')
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

csrf_exempt
@login_required(login_url="login")
def chat_messages(request):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")
        friend_username = data.get("friend")
        message_content = data.get("message")

        if action =="send" and friend_username and message_content:
            try:
                recipient = get_object_or_404(User, username=friend_username)
                new_message = Messages.objects.create(
                    sender=request.user,
                    recipient=recipient,
                    message=message_content
                )
                return JsonResponse({
                    "status": "success",
                    "message": {
                        "id": new_message.id,
                        "sender": request.user.username,
                        "recipient": friend_username,
                        "message": new_message.message,
                        "created_at": new_message.created_at.strftime("%I:%M %p"),
                    } 
                })
            except User.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Recipient not found."},status=501)
            
    elif request.method == "GET":
        friend_username = request.GET.get("friend")
        if friend_username:
            try:
                friend = get_object_or_404(User, username=friend_username)

                messages = Messages.objects.filter((
                        models.Q(sender=request.user, recipient=friend) | 
                        models.Q(sender=friend, recipient=request.user)
                    )).order_by("created_at")
                message_data = [{
                    "id": msg.id,
                    "sender": msg.sender.username,
                    "recipient": msg.recipient.username,
                    "message": msg.message,
                    "created_at": msg.created_at.strftime("%I:%M %p"),
                } for msg in messages]

                return JsonResponse({
                    "status": "success",
                    "messages": message_data,
                })
            except User.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)
        
    return JsonResponse({"status": "error", "message": "Invalid action."}, status=502)