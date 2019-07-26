from django.urls import path, re_path
from Buyer import views

urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('index/', views.index),
    path('logout/', views.logout),
    path('goods_list/', views.goods_list),
    path('goods_detail/', views.goods_detail),
]
urlpatterns += [
    re_path(r'^ajaxValid/(?P<data>\w+)/$', views.ajaxValid),
    path('pay_order/', views.pay_order),
    path('pay_result/', views.pay_result),
]