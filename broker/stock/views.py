from django.http.response import JsonResponse
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
        
        index_niftyBank = nse.get_index_quote("nifty bank")
        print(index_niftyBank)
        context['niftyBankPrice'] = index_niftyBank['lastPrice']
        return JsonResponse(context)

    return render(request, 'dashboard.html', {})