from django.db import models

# Create your models here.

class Investment(models.Model):
    buy_price = models.IntegerField(null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

class History(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    sell_price = models.IntegerField(null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)


