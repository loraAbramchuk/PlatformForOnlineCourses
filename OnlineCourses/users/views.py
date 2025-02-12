from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from main.models import Course

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html',  {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Получаем пользователя
            login(request, user)  # Авторизуем его
            return redirect('dashboard')  # Перенаправляем на главную страницу
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request):
    # Получаем пользователя
    user = request.user

    enrolled_courses = Course.objects.filter(students=user)

    return render(request, 'profile.html', {'user': user, 'enrolled_courses': enrolled_courses})
