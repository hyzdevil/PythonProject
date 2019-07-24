from django.urls import path,re_path
from Store import views

urlpatterns = [
    path('', views.index),
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.login_out),
    path('reset_password/', views.reset_password),
    path('register_store/', views.register_store),
    path('getProvince/', views.getProvince),
    path('getCity/', views.getCity),
    path('getDistrict/', views.getDistrict),
    path('add_goods/', views.add_goods),
    path('list_goods/', views.list_goods),
    re_path(r'^sold_out/(?P<goods_id>\d+)/$', views.sold_out),
    re_path(r'^putaway/(?P<goods_id>\d+)/$', views.putaway),
    re_path(r'^detail_goods/(?P<goods_id>\d+)/$', views.goods_detail),
    re_path(r'^update_goods/(?P<goods_id>\d+)/$', views.update_goods),
]