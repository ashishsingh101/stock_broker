from django.urls import path, include
from . import views

urlpatterns = [
    path('Profile/', views.profile, name="profile" ),
]
