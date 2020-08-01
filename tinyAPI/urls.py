from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('sendMessage/<query>/', views.sendQuery),
    path('createUser/<username>/<password>/<name>/<intent>/', views.createUser),
    path('adminLogin/<username>/<password>/', views.adminLogin),
]
# username, password, name, intent
