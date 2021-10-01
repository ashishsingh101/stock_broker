from django.shortcuts import render
from django.conf import settings

# Create your views here.
def dashboard(request):
    print(settings.BASE_DIR, 'ash')
    print(settings.STATICFILES_DIRS)
    print(settings.STATIC_ROOT, 'sin')

    return render(request, 'dashboard.html', {})