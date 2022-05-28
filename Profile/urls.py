from django.urls import path, include
from . import views

urlpatterns = [
    path('Profile/', views.profile, name="profile" ),
    path('Orders/', views.orders, name="orders" ),
    path('Brokerage/', views.brokerage, name="brokerage" ),
    path('Report/', views.report, name="report" ),
]

