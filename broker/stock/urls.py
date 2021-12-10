from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard" ),
    path('detail/<str:stock_name>/', views.detail, name="detail" ),
]

