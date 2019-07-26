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
    path('goods_type_list/', views.goods_type_list),
    path('add_goods_type/', views.add_goods_type),
    path('del_goodsType/', views.del_goodsType),
    re_path(r'^list_goods/(?P<state>\w+)/$', views.list_goods),
    re_path(r'^set_goods/(?P<state>\w+)/$', views.set_goods),
    re_path(r'^detail_goods/(?P<goods_id>\d+)/$', views.goods_detail),
    re_path(r'^update_goods/(?P<goods_id>\d+)/$', views.update_goods),
]