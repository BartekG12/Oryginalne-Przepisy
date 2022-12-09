from django.urls import path
from . import views

urlpatterns = [
    path('', views.przepisy, name="przepisy"),
    path('przepis/<str:pk>/', views.przepis, name="przepis"),
    path('tworzenie-przepisu/', views.tworzeniePrzepisu, name='tworzenie-przepisu'),
    path('aktualizacja-przepisu/<str:pk>/', views.aktualizacjaPrzepisu, name='aktualizacja-przepisu'),
    path('usuwanie-obiektu/<str:pk>/', views.usuwanieObiektu, name='usuwanie-obiektu'),
    path('prosba/<str:pk>/', views.prosba, name='prosba'),
]