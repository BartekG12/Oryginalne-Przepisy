from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Przepis, Tag
from .forms import ProsbaForm, PrzepisFormularz, ReviewForm

def przepisy(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    tags = Tag.objects.filter(name__icontains=search_query)

    przepisy = Przepis.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )

    page = request.GET.get('page')
    results = 6
    paginator = Paginator(przepisy, results)
    try:
        przepisy = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        przepisy = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        przepisy = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    context = {
        'przepisy': przepisy,
        'search_query': search_query,
        'paginator': paginator,
        'custom_range': custom_range,
    }
    return render(request, 'przepisy/przepisy.html', context)

def przepis(request, pk):
    przepis = Przepis.objects.get(id = pk)
    form = ReviewForm

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.przepis = przepis
        review.owner = request.user.profil
        review.save()

        przepis.getVoteCount

        messages.success(request, "Dodano ocenę!")
        return redirect('przepis', pk=przepis.id)
    
    context = {
        'przepis':przepis,
        'form':form,
    }
    return render(request, 'przepisy/pojedynczy-przepis.html', context)

def prosba(request, pk):
    
    # profil = request.user.profil
    # przepis = profil.przepis_set.get(id=pk)
    # form = PrzepisFormularz(instance=przepis)
    # if request.method == 'POST':
    #     form = PrzepisFormularz(request.POST, request.FILES, instance=przepis)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('przepisy')


    przepis = Przepis.objects.get(id = pk)
    form = ProsbaForm(instance=przepis)

    if request.method == "POST":
        form = ProsbaForm(request.POST, instance=przepis)
        przepis = form.save(commit=False)
        przepis.was_asked = True
        przepis.save()
        return redirect('przepis', pk=przepis.id)

    context = {
        'przepis':przepis,
        'form':form,
    }
    return render(request, 'przepisy/pojedynczy-przepis.html', context)

@login_required(login_url="login")
def tworzeniePrzepisu(request):
    profil = request.user.profil
    form = PrzepisFormularz()
    if request.method == 'POST':
        form = PrzepisFormularz(request.POST, request.FILES)
        if form.is_valid():
            przepis = form.save(commit=False)
            przepis.owner = profil
            przepis.save()
            return redirect('przepisy')
    context = {
        'form':form,
    }
    return render(request, "przepisy/formularzPrzepisu.html", context)

@login_required(login_url="login")
def aktualizacjaPrzepisu(request, pk):
    profil = request.user.profil
    przepis = profil.przepis_set.get(id=pk)
    form = PrzepisFormularz(instance=przepis)
    if request.method == 'POST':
        form = PrzepisFormularz(request.POST, request.FILES, instance=przepis)
        if form.is_valid():
            form.save()
            return redirect('przepisy')
    context = {
        'form':form,
    }
    return render(request, "przepisy/formularzPrzepisu.html", context)

@login_required(login_url="login")
def usuwanieObiektu(request, pk):
    profil = request.user.profil
    przepis = profil.przepis_set.get(id=pk)
    if request.method == 'POST':
        przepis.delete()
        return redirect('przepisy')

    context = {
        'obiekt': przepis,
    }
    return render(request, 'usuwanie-obiektu.html', context)