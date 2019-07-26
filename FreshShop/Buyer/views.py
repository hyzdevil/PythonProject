import json
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect

from Buyer.models import *
from Store.models import *
from Store.views import setPassword

# Create your views here.
def ajaxValid(request, data):
    result = {"message":""}
    if data == "name":
        username = request.GET.get("username")
        buyer = Buyer.objects.filter(username=username).first()
        if buyer:
            result["message"] = "该用户已存在"
        return JsonResponse(result)
    else:
        email = request.GET.get("email")
        buyer = Buyer.objects.filter(email=email).first()
        if buyer:
            result["message"] = "该邮箱已被注册"
        return JsonResponse(result)

def login(request):
    result = {"message":""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        buyer = Buyer.objects.filter(username=username).first()
        if buyer:
            if buyer.password == setPassword(password):
                response = HttpResponseRedirect("/buyer/index/")
                response.set_cookie("username", json.dumps(username))
                request.session["username"] = username
                request.session["buyer_id"] = buyer.id
                return response
            else:
                result["message"] = "用户名或密码错误"
        else:
            result["message"] = "该用户不存在"
    return render(request, 'buyer/login.html', locals())

def register(request):
    if request.method == "POST":
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        buyer = Buyer()
        buyer.username=username
        buyer.password=setPassword(password)
        buyer.email=email
        buyer.save()
        return HttpResponseRedirect("/buyer/login/")
    return render(request, 'buyer/register.html')

def index(request):
    goods_type_list = GoodsType.objects.all()
    return render(request, 'buyer/index.html', locals())

def logout(request):
    response = HttpResponseRedirect("/buyer/index/")
    response.delete_cookie("username")
    request.session.flush()
    return response