from django.contrib import admin
from .models import BuyShare, SellShare, History

# Register your models here.
admin.site.register(BuyShare)
admin.site.register(SellShare)
admin.site.register(History)