from django.urls import path
from Store import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('index/', views.index),
    path('logout/', views.login_out),
    path('register_store/', views.register_store),
    path('getProvince/', views.getProvince),
    path('getCity/', views.getCity),
    path('getDistrict/', views.getDistrict),
    path('add_goods/', views.add_goods),
    path('list_goods/', views.list_goods),
]