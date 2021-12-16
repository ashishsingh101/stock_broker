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
# Create your views here.
def my_redirect(url):
    print('hello', URL_ROOT)
    return redirect(URL_ROOT + url)

def LoginPage(request):

    user = request.user 
    if user.is_authenticated:
        return my_redirect("/")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
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
        pass 

    return render(request, 'signup.html', {})
