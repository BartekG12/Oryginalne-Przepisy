from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import TworzenieUzytkownika, FormularzProfil, MessageForm

from .models import Profil, Message

def loginPage(request):
    page =  'login'
    context = {'page':page}
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        # try:
        #     user = User.objects.get(username=username)
        # except:
        #     messages.error(request, "Nie ma takiego użytkownika")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'konto-uzytkownika')
        else:
            messages.error(request, "Nieprawidłowa nazwa użytkownika lub hasło")
    return render(request, 'uzytkownicy/login_register.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, "Wylogowano!")
    return redirect('login')

def register(request):
    page =  'register'
    form = TworzenieUzytkownika
    if request.method == 'POST':
        form = TworzenieUzytkownika(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Konto zostało założone!')
            login(request, user)
            return redirect('zmien-ustawienia')
        else:
            messages.error(request, 'Wprowadzono niepoprawne dane')
    context = {
        'page':page,
        'form':form
        }
    return render(request, 'uzytkownicy/login_register.html', context)

def profile(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    profile = Profil.objects.filter(Q(name__icontains=search_query) | Q(self_pitch__icontains=search_query))


    page = request.GET.get('page')
    results = 3
    paginator = Paginator(profile, results)
    try:
        profile = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profile = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profile = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)


    context = {
        'profile':profile,
        'search_query':search_query,
        'paginator': paginator,
        'custom_range': custom_range,
        }
    return render(request, 'uzytkownicy/profile.html', context)

def profilUzytkownika(request, pk):
    profile = Profil.objects.get(id=pk)
    context = { 'profil':profile }
    return render(request, 'uzytkownicy/profil-uzytkownika.html', context )

@login_required(login_url='login')
def kontoUzytkownika(request):
    profil = request.user.profil
    przepisy = profil.przepis_set.all()
    context = {
        'profil':profil,
        'przepisy':przepisy,
        }
    return render(request, 'uzytkownicy/account.html', context)

@login_required(login_url='login')
def zmienUstawienia(request):
    profile = request.user.profil
    form = FormularzProfil(instance=profile)
    if request.method == "POST":
        form = FormularzProfil(request.POST, request.FILES, instance=profile)
        if form.is_valid:
            form.save()

            return redirect('konto-uzytkownika')
    context = { 'form': form}
    return render(request, 'uzytkownicy/formularz-profil.html', context)

@login_required(login_url='login')
def inbox(request):
    profil = request.user.profil
    messageRequest = profil.messages.all()
    unreadCount = messageRequest.filter(was_read=False).count()
    context = {
        'messageRequest':messageRequest,
        'unreadCount':unreadCount,
    }
    return render(request, 'uzytkownicy/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profil = request.user.profil
    message = profil.messages.get(id=pk)
    if message.was_read == False:
        message.was_read = True
        message.save()
    context = {'message':message}
    return render(request, 'uzytkownicy/message.html', context)

def createMessage(request, pk):
    recipient = Profil.objects.get(id=pk)
    form = MessageForm()

    if request.user.is_authenticated:
        sender = request.user.profil
    else:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request, 'Wysłano wiadomość!')
            return redirect('profil-uzytkownika', pk=recipient.id)

    context = {
        'recipient':recipient,
        'form':form,
    }
    return render(request, 'uzytkownicy/message_form.html', context)
