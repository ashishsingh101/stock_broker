from django.contrib import admin
from .models import BuyShare, SellShare, History, HoldingPerStock, Report

# Register your models here.
admin.site.register(BuyShare)
admin.site.register(SellShare)
admin.site.register(History)
admin.site.register(HoldingPerStock)    
admin.site.register(Report)