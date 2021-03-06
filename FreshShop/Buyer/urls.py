from django.urls import path, re_path
from Buyer import views

urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('index/', views.index),
    path('logout/', views.logout),
    path('goods_list/', views.goods_list),
    path('goods_detail/', views.goods_detail),
    path('add_cart/', views.add_cart),
    path('cart/', views.cart),
    path('del_goods/', views.del_goods),
    path('place_order/', views.place_order),
    path('add_order/', views.add_order),
    path('user_order/', views.user_order),
    path('user_center/', views.user_center),
    path('user_site/', views.user_site),
]
urlpatterns += [
    re_path(r'^ajaxValid/(?P<data>\w+)/$', views.ajaxValid),
    path('pay_order/', views.pay_order),
    path('pay_result/', views.pay_result),
]