from django.contrib import admin
from django.urls import path, re_path
from django.http import HttpResponse
from . import views

def not_found_response(request):
    return HttpResponse('<h2>404 Not Found</h2>')

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_route, name="login"),
    path('logout', views.logout_route, name="logout"),
    path('register', views.register_route, name="register"),
    path("chat-app", views.chatapp, name="chat-app"),
    path('chat-app/user/<str:username>/', views.chatapp, name='chat-app-user'),
 


    # re_path(r'.*', not_found_response)
]
