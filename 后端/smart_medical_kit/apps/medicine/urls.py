from django.contrib import admin
from django.urls import path, include
from . import views
from .views import CreateMedical, ShowUserMedical, SearchMedicineView, DeleteMedicineView, SearchMedicineView2, \
    SearchMedicineView3, ShowMedical, ShowTime, SearchMedicineView4, ShowMedical2, ShowTime2, ImgageView

app_name = 'medicine'
urlpatterns = [
    path('medical/<str:name>/<str:token>/', CreateMedical.as_view(), name='createmedical'),
    path('showmedical/<str:token>/', ShowUserMedical.as_view(), name='showmedical'),
    path('search/<str:name>/', SearchMedicineView.as_view(), name='searchmedicine'),
    path('search2/<str:name>/', SearchMedicineView2.as_view(), name='searchmedicine2'),
    path('search3/<str:name>/', SearchMedicineView3.as_view(), name='searchmedicine3'),
    path('search4/<str:name>/', SearchMedicineView4.as_view(), name='searchmedicine4'),
    path('delete/<str:name>/<str:token>/', DeleteMedicineView.as_view(), name='deletemedicine'),
    path('show/<str:name>/', ShowMedical.as_view(), name='showmedicals'),
    path('show2/<str:name>/', ShowMedical2.as_view(), name='showmedicals2'),
    path('time/<str:token>/', ShowTime.as_view(), name='showtime'),
    path('time2/<str:token>/', ShowTime2.as_view(), name='showtime2'),
    path('imgtest/', ImgageView.as_view(), name='image'),
]
