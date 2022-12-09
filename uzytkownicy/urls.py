from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register, name='register'),

    path('', views.profile, name='profile'),
    path('profil/<str:pk>/', views.profilUzytkownika, name='profil-uzytkownika'),
    path('konto/', views.kontoUzytkownika, name='konto-uzytkownika'),
    
    path('zmien-ustawienia/', views.zmienUstawienia, name='zmien-ustawienia'),

    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.viewMessage, name='message'),
    path('create-message/<str:pk>', views.createMessage, name='create-message'),
]