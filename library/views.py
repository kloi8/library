from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Material, Discipline, SchoolClass, Profile
from .forms import MaterialForm
from django.core.paginator import Paginator

def index(request):
    # Если пользователь не авторизован ему доступна отдельная страница
    if not request.user.is_authenticated:
        return render(request, "library/welcome.html")
    profile = Profile.objects.filter(user=request.user).first()
    # query = request.GET.get('q','')
    query = request.GET.get("q", "").strip()
    discipline = request.GET.get('discipline','')
    class_id = request.GET.get('class','')
    materials = Material.objects.all().order_by("-created_at")



# Ученик видит только материалы своего класса
    if profile.role == "student":
        materials = materials.filter(school_class=profile.school_class)

# Преподаватель видит материалы только своей дисциплины
    elif profile.role == "teacher":
        materials = materials.filter(discipline=profile.discipline)








# РАБОЧИЙ
    if query:
        words = query.strip().split()

        for word in words:
            materials = materials.filter(
                models.Q(title__icontains=word) |
                models.Q(author__icontains=word)
            )



        # Ученик → может фильтровать ТОЛЬКО по дисциплинам
    if profile.role == "student":
        if discipline:
            materials = materials.filter(discipline_id=discipline)

    # Преподаватель → может фильтровать ТОЛЬКО по классам
    elif profile.role == "teacher":
        if class_id:
            materials = materials.filter(school_class_id=class_id)

    # Администратор → может фильтровать по предмету и классу
    elif profile.role == "admin":
        if discipline:
            materials = materials.filter(discipline_id=discipline)
        if class_id:
            materials = materials.filter(school_class_id=class_id)


    paginator = Paginator(materials, 10)
    page = request.GET.get('page')
    materials = paginator.get_page(page)
    return render(request,'library/index.html',{'materials':materials,'disciplines':Discipline.objects.all(),'classes':SchoolClass.objects.all(),'profile':profile,'query':query})

def material_view(request, pk):
    mat = get_object_or_404(Material, pk=pk)
    return render(request,'library/material_view.html',{'material':mat})

@login_required
def add_material(request):
    if not hasattr(request.user,'profile') or request.user.profile.role not in ['teacher','admin']:
        return redirect('index')
    if request.method=='POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            m = form.save(commit=False)
            m.uploaded_by = request.user
            m.save()
            return redirect('index')
    else:
        form = MaterialForm()
    return render(request,'library/add_material.html',{'form':form})

def user_login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
    return render(request,'library/login.html')

def user_logout(request):
    logout(request)
    return redirect('index')
