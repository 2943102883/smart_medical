from django.contrib import admin
from django.urls import path, include

from . import views
from .views import ShowUserMessage, Create_or_LoginView

app_name = 'user'
urlpatterns = [
    # path('createuser/<str:token>/', CreateUser.as_view(), name='createuser'),
    path('showuser/<str:token>/', ShowUserMessage.as_view(), name='showuser'),
    path('loginORcreate/', Create_or_LoginView.as_view(), name='create_or_login'),
]
