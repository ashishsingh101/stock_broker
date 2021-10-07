from django.shortcuts import render
from django.conf import settings

# Create your views here.
def dashboard(request):

    return render(request, 'dashboard.html', {})