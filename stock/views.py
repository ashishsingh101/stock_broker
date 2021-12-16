from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from nsetools import Nse
import nsepy
from datetime import date
import json
import pandas as pd

# Create your views here.
def dashboard(request):

    if request.method == "POST" and request.POST['action']=='dashboard_data':
        context = {}
        nse = Nse()
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
        
        d=context['topGainers'][0]
        """
        for ele in d:
            print(ele+' : '+str(d[ele]))
        """
        logos = {}
        for ele in context['topGainers']:
            logos[ele['symbol']] = nse.get_quote(ele['symbol'])['isinCode']
        for ele in context['topLosers']:
            logos[ele['symbol']] = nse.get_quote(ele['symbol'])['isinCode']
        context['logos'] = logos
        """
        d=nse.get_quote('ZOMATO')
        for ele in d:
            print(ele)
        """ 
        return JsonResponse(context)

    return render(request, 'dashboard.html', {})

def detail(request, stock_name):

    if request.method == 'POST' and request.POST['action']=='chart_data':
        print('pass')
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
            one_month_data.append([int(dates[i].strftime('%s')), [open[i], high[i], low[i], close[i]]])
        """
        for data in nsepy.get_history(symbol=stock_name, start=one_month_ago, end=today):
            one_month_data.append(['', data.open, data.high, data.low, data.close])
        """

        context = {
            'one_month_data' : one_month_data,
            'stock' : nse.get_quote(stock_name),
        }
        return JsonResponse(context)

    return render(request, 'detail.html', {})