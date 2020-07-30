from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('sendMessage/<query>/', views.sendQuery),
]
