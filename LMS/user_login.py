from django.shortcuts import redirect, render
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def REGISTER(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # check email
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists!')
            return redirect('register')

        # check username
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists!')
            return redirect('register')

        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return redirect('login')

    return render(request, 'registration/register.html')


def DO_LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = EmailBackEnd.authenticate(request,
                                         username=email,
                                         password=password)

        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email and Password Are Invalid !')
            return redirect('login')

def PROFILE(request):
    return render(request,'registration/profile.html')

def PROFILE_UPDATE(request):

    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_id = request.user.id

        try:
            user = User.objects.get(id=user_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email

            if password and password.strip() != "":
                user.set_password(password)

            user.save()
            messages.success(request, 'Profile Successfully Updated.')
            return redirect('profile')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('profile')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('profile')

        return render(request, 'registration/profile_update.html')