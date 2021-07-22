from django.contrib import admin
from django.urls import path, include
from . import views
from .views import ShowIOTs, KTView

app_name = 'iot'
urlpatterns = [
    path('showiot/', ShowIOTs.as_view(), name='showiot'),
    path('kt/', KTView.as_view(), name='kt'),
]
