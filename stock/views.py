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

from users.models import CustomUser
from .models import BuyShare, HoldingPerStock, History, Report
from .models import all_stocks 
from django.utils import timezone

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
    #print(timezone.localtime())
    #print(datetime.datetime.now())

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
        shares_holding = 0
        if HoldingPerStock.objects.filter(user=user, share_symbol=stock_name).exists():
            shares_holding = HoldingPerStock.objects.get(user=user, share_symbol=stock_name).quantity

        context = {
            'one_month_data' : one_month_data,
            'stock' : nse.get_quote(stock_name),
            'shares_holding' : shares_holding,
        }
        return JsonResponse(context)

    if request.method == 'POST' and request.POST['action']=='Buy':
        #print(request.POST)
        custom_user = CustomUser.objects.get(user=user)
        
        if request.POST['quantity'] == '' or int(request.POST['quantity']) <= 0:
            return JsonResponse({'status': 'noshare'})

        buy_price = float(request.POST['price'])*int(request.POST['quantity'])  # total price (price*quantity)
        equity_brokerage = min( (buy_price*0.05)/100, 20 ) 
        stt = (buy_price*0.1)/100
        stamp_duty = (buy_price*0.015)/100 
        exchange_transaction = (buy_price*0.00345)/100
        sebi_turnover = (buy_price*0.0001)/100
        gst = ((equity_brokerage+exchange_transaction)*18)/100

        if buy_price + equity_brokerage + stt + stamp_duty + exchange_transaction + sebi_turnover + gst > custom_user.wallet:
            return JsonResponse({'status': 'notenough_money'})

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

        '''update report and wallet'''
        new_report = Report.objects.create(user=user, buy_price=request.POST['price'], share_symbol=request.POST['stock'], buy_share=int(request.POST['quantity']), equity_brokerage=equity_brokerage, stt=stt, stamp_duty=stamp_duty, exchange_transaction=exchange_transaction, sebi_turnover=sebi_turnover, gst=gst)
        new_report.save()
        custom_user.wallet -= buy_price + equity_brokerage + stt + stamp_duty + exchange_transaction + sebi_turnover + gst
        custom_user.save()

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
                '''remove shares from BuyShare table'''
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
                '''remove shares from HoldingPerStock table'''
                if existed_holding.quantity == int(request.POST['quantity']):
                    existed_holding.delete()
                else:
                    existed_holding.quantity -= int(request.POST['quantity'])
                    existed_holding.save()

                '''update report table for respective shares selled'''
                equity_brokerage = min((float(request.POST['price'])*int(request.POST['quantity']))*0.05/100, 20)
                exchange_transaction = ((float(request.POST['price'])*int(request.POST['quantity']))*0.00345)/100
                sebi_turnover = ((float(request.POST['price'])*int(request.POST['quantity']))*0.0001)/100
                gst = ((equity_brokerage+exchange_transaction+13.5)*18)/100

                sell_share = int(request.POST['quantity'])
                for update_report in Report.objects.filter(user=user, share_symbol=request.POST['stock']).order_by('buy_date'):
                    if update_report.sell_share:
                        sell = min(sell_share, int(update_report.buy_share - update_report.sell_share))
                    else:
                        sell = min(sell_share, int(update_report.buy_share))
                    if sell == 0:
                        continue
                    sell_share -= sell
                    if update_report.sell_share: # if sell_share is not empty then average the price
                        updated_sell_price = (update_report.sell_price*update_report.sell_share + float(request.POST['price'])*sell)/(update_report.sell_share+sell)
                        update_report.sell_price = updated_sell_price
                        update_report.sell_share += sell
                    else:
                        update_report.sell_price = float(request.POST['price'])
                        update_report.sell_share = sell
                    update_report.equity_brokerage += equity_brokerage
                    update_report.exchange_transaction += exchange_transaction
                    update_report.sebi_turnover += sebi_turnover
                    update_report.gst += gst
                    update_report.profit_loss = (update_report.sell_price - update_report.buy_price)*update_report.sell_share
                    update_report.save()
                    if sell_share == 0:
                        break

                '''update wallet'''
                custom_user = CustomUser.objects.get(user=user)
                custom_user.wallet += float(request.POST['price'])*int(request.POST['quantity']) - equity_brokerage - exchange_transaction - sebi_turnover - gst - 13.5
                custom_user.save()
                '''
                update_report = Report.objects.get(user=user, share_symbol=request.POST['stock'])
                if update_report.sell_share: # if sell_share is not empty then average the price
                    updated_sell_price = (update_report.sell_price*update_report.sell_share + float(request.POST['price'])*int(request.POST['quantity']))/(update_report.sell_share+int(request.POST['quantity']))
                    update_report.sell_price = updated_sell_price
                    update_report.sell_share += int(request.POST['quantity'])
                else:
                    update_report.sell_price = float(request.POST['price'])
                    update_report.sell_share = int(request.POST['quantity'])
                update_report.equity_brokerage += equity_brokerage
                update_report.exchange_transaction += exchange_transaction
                update_report.sebi_turnover += sebi_turnover
                update_report.gst += gst
                update_report.profit = (update_report.sell_price - update_report.buy_price)*update_report.sell_share
                update_report.save() 
                '''
                
        else:
            return JsonResponse({'status': 'not_inuf_share'})

        new_history = History.objects.create(user=user, share_symbol=request.POST['stock'], sell_price=request.POST['price'], quantity=int(request.POST['quantity']))
        new_history.save()

        status = 'success'
        return JsonResponse({'status':status})

    return render(request, 'detail.html', {})
