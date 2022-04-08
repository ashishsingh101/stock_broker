from multiprocessing import context
from django.http import request
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, TemplateView
from .models import CustomUser
import logging
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect 
from broker.settings import URL_ROOT
from django.contrib.auth import logout

# Create your views here.
def my_redirect(url):
    #print('hello', URL_ROOT)
    return redirect(URL_ROOT + url)

def LoginPage(request):

    user = request.user 
    if user.is_authenticated:
        return my_redirect("/")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return my_redirect('/')
        else:
            return my_redirect('/login/')

    return render(request, 'login.html', {})

def SignupPage(request):

    user = request.user 
    if user.is_authenticated:
        return my_redirect("/")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        firstName = request.POST['firstname']
        lastName = request.POST['lastname']

        if User.objects.filter(email=email).exists():
            print('email exists')
            return render(request, 'signup.html', {'email_exists': True})

        extra_value_username = False
        integer_in_username = False
        char_in_username = False
        user_exists = User.objects.filter(username=username).exists()
        for ch in username:
            if ch.isdigit():
                integer_in_username = True
            elif ch.isalpha():
                char_in_username = True
            else:
                extra_value_username = True
                break
        if user_exists:
            print('user exists')
            return render(request, 'signup.html', {'user_exists':True})
        if extra_value_username or not char_in_username or len(username)<6 or len(username)>18:
            print('username error')
            return render(request, 'signup.html', {'username_err': True})

        extra_value_password = False
        integer_in_password = False
        char_in_password = False
        special_in_password = False
        for ch in password:
            if ch.isdigit():
                integer_in_password = True
            elif ch.isalpha():
                char_in_password = True
            elif (ord(ch)>=33 and ord(ch)<=47) or (ord(ch)>=58 and ord(ch)<=64) or (ord(ch)>=91 and ord(ch)<=96) or (ord(ch)>=123 and ord(ch)<=126):
                special_in_password = True
            else:
                extra_value_password = True
                break
        if not char_in_password or not integer_in_password or not special_in_password or len(password)<6 or len(password)>18 or extra_value_password:
            return render(request, 'signup.html', {'password_err': True})

        new_user = User.objects.create_user(username=username, password=password, email=email, first_name=firstName, last_name=lastName)
        new_custom_user = CustomUser.objects.create(user=new_user)
        new_custom_user.save()

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return my_redirect('/')
        else:
            return my_redirect('/Signup/')

    context = {'username_err': False, 'password_err':False }
    return render(request, 'signup.html', context)

def LogoutUser(request):
    logout(request)
    return my_redirect('/login/')
