from multiprocessing import context
from django.shortcuts import render
from users.models import CustomUser
from stock.models import BuyShare, HoldingPerStock
from django.http.response import HttpResponse, JsonResponse
from stock.models import History
from nsetools import Nse

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

def brokerage(request):
    user = request.user
    context = {}

    return render(request, 'brokerage.html', context)

def report(request):
    user = request.user
    nse = Nse()

    symbol = []
    name = []
    avg_buy = []
    percentage_change = []
    price_change = []
    total_shares = []
    total_cost = []
    market_value = []
    gain = []
    returns = []

    price_change_greater = []
    gain_profit = []
    returns_profit = []

    for holding in HoldingPerStock.objects.filter(user=user):  
        avgBuy = 0
        totalCost = 0
        totalShares = 0

        for buy in BuyShare.objects.filter(user=user, share_symbol=holding.share_symbol).order_by('-date_time'):
            totalCost += buy.buy_price * buy.quantity
            totalShares += buy.quantity

        share_detail = nse.get_quote(holding.share_symbol)
        avgBuy = totalCost / totalShares
        avg_buy.append(round(avgBuy, 2))
        symbol.append(holding.share_symbol)
        name.append(share_detail['companyName'])
        percentage_change.append(share_detail['pChange'])
        price_change.append(share_detail['change'])
        total_shares.append(totalShares)
        total_cost.append(round(totalCost,2))
        market_value.append(round(totalShares * share_detail['lastPrice'], 2))
        gain.append(round((totalShares * share_detail['lastPrice']) - totalCost, 2))
        returns.append(round(((share_detail['lastPrice'] - avgBuy)/avgBuy)*100, 2))

        if float(share_detail['pChange']) > 0.0:
            price_change_greater.append(True)
        else:
            price_change_greater.append(False)
        if float(round((totalShares * share_detail['lastPrice']) - totalCost)) > 0.0:
            gain_profit.append(True)
        else:
            gain_profit.append(False)
        if round(((share_detail['lastPrice'] - avgBuy)/avgBuy)*100, 2) > 0.0:
            returns_profit.append(True)
        else:
            returns_profit.append(False)
    
    context = {
        'symbol' : symbol,
        'name' : name,
        'avg_buy' : avg_buy,
        'percentage_change' : zip(percentage_change,price_change_greater),
        'price_change' : zip(price_change,price_change_greater),
        'total_shares' : total_shares,
        'total_cost' : total_cost,
        'market_value' : market_value,
        'gain' : zip(gain, gain_profit),
        'returns' : zip(returns, returns_profit),
        'price_change_greater' : price_change_greater
    }

    return render(request, 'report.html', context)