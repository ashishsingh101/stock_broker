from django.http import request
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, TemplateView
from .models import CustomUser
import logging
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect 
from broker.settings import URL_ROOT

# Create your views here.
def my_redirect(url):
    return redirect(URL_ROOT + url)

def LoginPage(request):

    if request.method == 'POST' and request.POST['action'] == 'login':
        user = request.POST['user']
        password = request.POST['password']
        print(user, password)

        user = authenticate(username=user, password=password)
        if user is not None:
            return my_redirect('/')
        else:
            return my_redirect('/login/')

    return render(request, 'login.html', {})

def SignupPage(request):
    return render(request, 'signup.html', {})
