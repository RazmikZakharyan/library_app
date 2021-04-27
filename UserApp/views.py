from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from .forms import UserRegisterForm, UserAuthenticationForm


def user_register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print()
        if form.is_valid():
            form.save()
            user = UserAuthenticationForm(data={'username': form.username, 'password': form.password1}).get_user()
            login(request, user)
            return redirect('home')
        else:
            for item in eval(form.errors.as_json()).values():
                messages.error(request, item[0]['message'])
    else:
        form = UserRegisterForm()
    return render(request, 'UserApp/register.html', {'form': form})


def user_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')
    if request.method == 'POST':
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password not correct')
    else:
        form = UserAuthenticationForm()
    return render(request, 'UserApp/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')
