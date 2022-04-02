from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from nsetools import Nse
import nsepy
from datetime import date
import json
import pandas as pd
import time, datetime
from broker.settings import URL_ROOT
from django.shortcuts import redirect
from .models import BuyShare, HoldingPerStock, History
from .models import all_stocks 

# Create your views here.

def my_redirect(url):
    #print('hello', URL_ROOT)
    return redirect(URL_ROOT + url)


def dashboard(request):
    user = request.user

    if not user.is_authenticated:
        return my_redirect('/login/')
    holdings = HoldingPerStock.objects.filter(user=user)

    if request.method == "POST" and request.POST['action']=='dashboard_data':
        context = {}
        nse = Nse()
        #print(nse.get_stock_codes().keys())  # prints all the stock codes 

        index_nifty = nse.get_index_quote("nifty 50")
        context['niftyPrice'] = index_nifty['lastPrice']
        context['niftyChange'] = index_nifty['change']
        context['niftyPChange'] = index_nifty['pChange']
        
        index_niftyBank = nse.get_index_quote("nifty bank")
        context['niftyBankPrice'] = index_niftyBank['lastPrice']
        context['niftyBankChange'] = index_niftyBank['change']
        context['niftyBankPChange'] = index_niftyBank['pChange']

        context['topGainers'] = nse.get_top_gainers()[:5]
        context['topLosers'] = nse.get_top_losers()[:5]

        logos = {}
        for ele in context['topGainers']:
            logos[ele['symbol']] = nse.get_quote(ele['symbol'])['isinCode']
        for ele in context['topLosers']:
            logos[ele['symbol']] = nse.get_quote(ele['symbol'])['isinCode']
        context['logos'] = logos

        return JsonResponse(context)
    
    return render(request, 'dashboard.html', {'holdings': holdings, 'all_stocks': all_stocks})

def detail(request, stock_name):
    user = request.user

    if not user.is_authenticated:
        return my_redirect('/login/')

    if request.method == 'POST' and request.POST['action']=='chart_data':
        #print('pass')
        nse = Nse()
        today = date.today()
        one_month_ago = today.replace(year=today.year-1)
        """
        if today.month == 1:
            one_month_ago = today.replace(year=today.year-1, month=12)
        elif today.day > 28:
            one_month_ago = today.replace(month=today.month-1, day=28)
        else:
            one_month_ago = today.replace(month=today.month-1)
        """
        one_month_data = nsepy.get_history(symbol=stock_name, start=one_month_ago, end=today)
        one_month_data = one_month_data[['Open','High', 'Low', 'Close']]
        df = pd.DataFrame(one_month_data)
        #print(df.index)
        dates = df.index.tolist()
        open = df['Open'].values.tolist()
        high = df['High'].values.tolist()
        low = df['Low'].values.tolist()
        close = df['Close'].values.tolist()
        #print(nsepy.get_history(symbol=stock_name, start=date(2015,1,1), end=date(2015,1,31)))
        one_month_data = [] # date, open, high, low, close
        for i in range(len(dates)):
            one_month_data.append([time.mktime(datetime.datetime.strptime(str(dates[i]), "%Y-%m-%d").timetuple()), [open[i], high[i], low[i], close[i]]])
        """
        for data in nsepy.get_history(symbol=stock_name, start=one_month_ago, end=today):
            one_month_data.append(['', data.open, data.high, data.low, data.close])
        """

        context = {
            'one_month_data' : one_month_data,
            'stock' : nse.get_quote(stock_name),
        }
        return JsonResponse(context)

    if request.method == 'POST' and request.POST['action']=='Buy':
        print(request.POST)
        
        if request.POST['quantity'] == '' or int(request.POST['quantity']) <= 0:
            return JsonResponse({'status': 'noshare'})

        new_buy_data = BuyShare.objects.create(user=user, buy_price=request.POST['price'], share_symbol=request.POST['stock'], quantity=int(request.POST['quantity']))
        new_buy_data.save()
        
        if HoldingPerStock.objects.filter(user=user, share_symbol=request.POST['stock']).exists():
            existed_holding = HoldingPerStock.objects.get(user=user, share_symbol=request.POST['stock'])
            existed_holding.quantity += int(request.POST['quantity'])
            existed_holding.save()
        else:
            new_holding = HoldingPerStock.objects.create(user=user, share_symbol=request.POST['stock'], quantity=int(request.POST['quantity']))
            new_holding.save()

        new_history = History.objects.create(user=user, share_symbol=request.POST['stock'], buy_price=request.POST['price'], quantity=int(request.POST['quantity']))
        new_history.save()

        status = 'success'
        return JsonResponse({'status':status})

    if request.method == 'POST' and request.POST['action']=='Sell':
        print(request.POST)
        if request.POST['quantity'] == '' or int(request.POST['quantity']) <= 0:
            return JsonResponse({'status': 'noshare'})

        if HoldingPerStock.objects.filter(user=user, share_symbol=request.POST['stock']).exists():
            existed_holding = HoldingPerStock.objects.get(user=user, share_symbol=request.POST['stock'])
            if existed_holding.quantity < int(request.POST['quantity']):
                return JsonResponse({'status': 'not_inuf_share'})
            else:
                sell_share = int(request.POST['quantity'])
                for buyed_share in BuyShare.objects.filter(user=user, share_symbol=request.POST['stock']).order_by('date_time'):
                    if sell_share >= buyed_share.quantity:
                        sell_share -= buyed_share.quantity
                        buyed_share.delete()
                        if sell_share == 0:
                            break
                    else:
                        buyed_share.quantity -= sell_share
                        buyed_share.save()
                        sell_share = 0
                        break
                
                if existed_holding.quantity == int(request.POST['quantity']):
                    existed_holding.delete()
                else:
                    existed_holding.quantity -= int(request.POST['quantity'])
                    existed_holding.save()
        else:
            return JsonResponse({'status': 'not_inuf_share'})

        new_history = History.objects.create(user=user, share_symbol=request.POST['stock'], sell_price=request.POST['price'], quantity=int(request.POST['quantity']))
        new_history.save()

        status = 'success'
        return JsonResponse({'status':status})

    return render(request, 'detail.html', {})
