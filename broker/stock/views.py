from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from nsetools import Nse

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

def detail(request):

    if request.method == 'GET':
        print(request.GET['stock_name'])

    return render(request, 'detail.html', {})