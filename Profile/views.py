from multiprocessing import context
from django.shortcuts import render
from users.models import CustomUser
from stock.models import HoldingPerStock
from django.http.response import HttpResponse, JsonResponse
from stock.models import History

# Create your views here.

def profile(request):
    user = request.user

    if request.method == 'POST' and request.POST['action']=='profile_data':
        context = {}
        holdings = {}
        names = []
        quantity = []
        for holding in HoldingPerStock.objects.filter(user=user):
            names.append(holding.share_symbol)
            quantity.append(holding.quantity)
        if len(names) > 0:
            holdings['names'] = names
            holdings['quantity'] = quantity
        else:
            holdings['names'] = ['no holdings']
            holdings['quantity'] = [100]
        context['holdings'] = holdings

        user_detail = CustomUser.objects.get(user=user)

        details = {}
        details['name'] = user.first_name + ' ' + user.last_name
        details['email'] = user.email
        details['phone'] = str(user_detail.phoneNumber)
        details['dob'] = user_detail.dateOfBirth
        details['gender'] = user_detail.gender
        details['uuid'] = user_detail.uniqueCode
        details['wallet'] = user_detail.wallet
        context['details'] = details

        return JsonResponse(context)
    return render(request, 'profile.html', {})

def orders(request):
    user = request.user
    context = {}

    all_orders = History.objects.filter(user=user).order_by('-date_time')
    context['all_orders'] = all_orders

    return render(request, 'orders.html', context)