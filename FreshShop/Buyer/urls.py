from django.urls import path, re_path
from Buyer import views

urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('index/', views.index),
    path('logout/', views.logout),
]
urlpatterns += [
    re_path(r'^ajaxValid/(?P<data>\w+)/$', views.ajaxValid),
]