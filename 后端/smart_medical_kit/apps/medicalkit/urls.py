from django.contrib import admin
from django.urls import path, include
from . import views
from .views import TestView, ShowSelfMedical

app_name = 'medicalkit'
urlpatterns = [
    path('test/', TestView.as_view(), name='test'),
    path('showall/', ShowSelfMedical.as_view(), name='showall'),
]
