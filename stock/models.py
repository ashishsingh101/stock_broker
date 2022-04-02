from django.db import models
from users.models import CustomUser
from django.contrib.auth.models import User
from nsetools import Nse

# Create your models here.
nse = Nse()
all_stocks = list(nse.get_stock_codes().keys())


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share_symbol = models.CharField(max_length=100)
    buy_price = models.FloatField(null=True)
    sell_price = models.FloatField(null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=True)

# class TranactionHistory(models.Model):


'''
class BuySell(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    buy_price = models.IntegerField(null=True, blank=True)
    sell_price = models.IntegerField(null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
'''


class BuyShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buy_price = models.FloatField()
    date_time = models.DateTimeField(auto_now_add=True)
    share_symbol = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.user.username


class SellShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sell_price = models.FloatField()
    date_time = models.DateTimeField(auto_now_add=True)
    share_symbol = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.user.username


class HoldingPerStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share_symbol = models.CharField(max_length=100)
    quantity = models.IntegerField()
