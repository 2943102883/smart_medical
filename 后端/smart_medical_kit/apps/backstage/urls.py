from django.contrib import admin
from django.urls import path, include
from . import views
from .views import MessageView, RegisterUser, UserView, UserCollectView, PeopleliveView, ChinaView

app_name = 'backstage'
urlpatterns = [
    path('usernum/', RegisterUser.as_view(), name='usernumber'),
    path('user/', UserView.as_view(), name='usermessage'),
    path('usercollect/', UserCollectView.as_view(), name='usercollect'),
    path('live/', PeopleliveView.as_view(), name='peoplelive'),
    path('map/', ChinaView.as_view(), name='map')
]
