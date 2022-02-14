from django.shortcuts import render
from users.models import CustomUser

# Create your views here.

def profile(request):
    user = request.user
    context = {}

    print(user.first_name, user.last_name)
    print(user.email)
    custom_user = CustomUser.objects.get(user=user)


    return render(request, 'profile.html', {})