from django.shortcuts import render
from users.models import CustomUser
from stock.models import HoldingPerStock
from django.http.response import HttpResponse, JsonResponse

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
        return JsonResponse(context)
    return render(request, 'profile.html', {})