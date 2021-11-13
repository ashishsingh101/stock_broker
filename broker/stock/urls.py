from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard" ),
    path('detail/', views.detail, name="detail" ),
]

