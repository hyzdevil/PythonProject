import json
import hashlib

from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render,HttpResponseRedirect

from Store.models import *

# Create your views here.
""" 地址选择 """
# 获取省份信息
def getProvince(request):
    provinces = Area.objects.filter(aparent__isnull=True)
    res = []
    for i in provinces:
        res.append([i.id, i.atitle])
    return JsonResponse({"provinces":res})
# 获取市信息
def getCity(request):
    city_id = request.GET.get('city_id')
    cities = Area.objects.filter(aparent_id=city_id)
    res = []
    for i in cities:
        res.append([i.id, i.atitle])
    return JsonResponse({"cities":res})
# 获取县信息
def getDistrict(request):
    district_id = request.GET.get('district_id')
    cities = Area.objects.filter(aparent_id=district_id)
    res = []
    for i in cities:
        res.append([i.id, i.atitle])
    return JsonResponse({'district': res})
# 密码加密功能
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()
# 注册
def register(request):
    result = {"message":""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        apassword = request.POST.get("apassword")
        if username and password and apassword:
            user = Seller.objects.filter(username=username).first()
            if user:
                result["message"] = "用户名已被注册"
                return render(request, 'store/register.html', locals())
            if password == apassword:
                Seller.objects.create(
                    username=username,
                    password=setPassword(password),
                    nickname=username
                )
                return HttpResponseRedirect("/store/login/")
            else:
                result["message"] = "两次输入密码不一致"
        else:
            result["message"] = "注册信息不能为空"
    return render(request, 'store/register.html', locals())
# 登录
def login(request):
    result = {"message": ""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = Seller.objects.filter(username=username).first()
            if user:
                if user.password == setPassword(password):
                    response = HttpResponseRedirect('/store/index/')
                    response.set_cookie("username", json.dumps(username))
                    request.session["username"] = username
                    request.session["user_id"] = user.id
                    return response
                else:
                    result["message"] = "用户名或密码错误"
            else:
                result["message"] = "用户名不存在"
        else:
            result["message"] = "登录信息不能为空"
    return render(request, 'store/login.html', locals())
# 登录验证
def loginValid(fun):
    def inner(request, *args, **kwargs):
        c_name = request.COOKIES.get("username")
        s_name = request.session.get("username")
        if c_name and s_name:
            c_name = json.loads(c_name)
            user = Seller.objects.filter(username=c_name).first()
            if user and user.username == c_name:
                return fun(request, *args, **kwargs)
        return HttpResponseRedirect("/store/login/")
    return inner
# 首页
@loginValid
def index(request):
    return render(request, 'store/index.html', locals())
# 退出
def login_out(request):
    response = HttpResponseRedirect("/store/login/")
    response.delete_cookie("username")
    request.session.flush()
    return response
# 注册店铺
@loginValid
def register_store(request):
    storeType = StoreType.objects.all()
    if request.method == "POST":
        user_id = int(request.session.get("user_id"))
        store_name = request.POST.get("store_name")
        store_description = request.POST.get("store_description")
        store_phone = request.POST.get("store_phone")
        store_money = request.POST.get("store_money")
        store_logo = request.FILES.get("store_logo")
        store_type = request.POST.getlist("store_type")
        province_id = request.POST.get('province')
        city_id = request.POST.get('city')
        district_id = request.POST.get('district')
        province = Area.objects.get(id=province_id)
        city = Area.objects.get(id=city_id)
        district = Area.objects.get(id=district_id)
        detail = request.POST.get('detail')
        store_address = str(province) + str(city) + str(district) + str(detail)
        store = Store()
        store.store_name = store_name
        store.store_description = store_description
        store.store_phone = store_phone
        store.store_money = store_money
        store.store_logo = store_logo
        store.store_address = store_address
        store.user = Seller.objects.filter(id=user_id).first()
        store.save()
        for i in store_type:
            store.type.add(StoreType.objects.get(id=i))
        store.save()
        return HttpResponseRedirect("/store/index/")
    return render(request, "store/register_store.html", {"storeType":storeType})
# 添加商品
@loginValid
def add_goods(request):
    user_id = request.session.get("user_id")
    store = Store.objects.filter(user_id=user_id)
    goods_type_list = GoodsType.objects.all()
    if request.method == "POST":
        goods_name = request.POST.get("goods_name")
        goods_description = request.POST.get("goods_description")
        goods_price = request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_images = request.FILES.get("goods_images")
        goods_date = request.POST.get("goods_date")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods_type = request.POST.get("goods_type")
        store_type = request.POST.getlist("store_type")
        goods = Goods()
        goods.goods_name = goods_name
        goods.goods_description = goods_description
        goods.goods_price = float(goods_price)
        goods.goods_number = goods_number
        goods.goods_images = goods_images
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_type_id = goods_type
        goods.save()
        for i in store_type:
            goods.store_id.add(Store.objects.get(id=i))
        goods.save()
        return HttpResponseRedirect("/store/list_goods/up/")
    return render(request, 'store/add_goods.html', {"store":store,"type_list":goods_type_list})
# 商品列表
@loginValid
def list_goods(request, state):
    if state == "up":
        status = 1
    else:
        status = 0
    keywords = request.GET.get("keywords","")
    page_num = request.GET.get("page_num", 1)
    store = Store.objects.filter(id=request.session.get("user_id"))
    goods_list = []
    if keywords:
        for i in store:
            goods = i.goods_set.filter(goods_name__contains=keywords, goods_status=status)
            goods_list += goods
    else:
        for i in store:
            goods = i.goods_set.filter(goods_status=status)
            goods_list += goods
    goods_list = list(set(goods_list))
    paginator = Paginator(goods_list, 10)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request, 'store/goods_list.html', locals())
# 商品详情
@loginValid
def goods_detail(request, goods_id):
    # user_id = request.session.get("user_id")
    # store = Store.objects.filter(user_id=user_id)
    goods_type_list = GoodsType.objects.all()
    goods = Goods.objects.filter(id = goods_id).first()
    return render(request, 'store/goods_detail.html', locals())
# 修改商品
@loginValid
def update_goods(request, goods_id):
    user_id = request.session.get("user_id")
    store = Store.objects.filter(user_id=user_id)
    goods = Goods.objects.filter(id = goods_id).first()
    if request.method == "POST":
        goods_name = request.POST.get("goods_name")
        goods_description = request.POST.get("goods_description")
        goods_price = request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_images = request.FILES.get("goods_images")
        goods_date = request.POST.get("goods_date")
        goods_safeDate = request.POST.get("goods_safeDate")
        store_type = request.POST.getlist("store_type")
        goods = Goods.objects.get(id=int(goods_id))
        goods.goods_name = goods_name
        goods.goods_description = goods_description
        goods.goods_price = float(goods_price)
        goods.goods_number = goods_number
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        if goods_images:
            goods.goods_images = goods_images
        goods.save()
        if store_type:
            goods.store_id.clear()
            for i in store_type:
                goods.store_id.add(Store.objects.get(id=i))
        goods.save()
        return HttpResponseRedirect("/store/detail_goods/%s/"%goods_id)
    return render(request, "store/update_goods.html", locals())
# 找回密码
def reset_password(request):
    return render(request, 'store/forgot_password.html')
# 设置商品状态
def set_goods(request, state):
    if state == "up":
        status = 1
    else:
        status = 0
    goods_id = request.GET.get("goods_id")
    referer = request.META.get("HTTP_REFERER")
    if goods_id:
        goods = Goods.objects.get(id = int(goods_id))
        if state == "delete":
            goods.delete()
        else:
            goods.goods_status = status
            goods.save()
    return HttpResponseRedirect(referer)
# 商品类别列表
def goods_type_list(request):
    page_num = request.GET.get("page_num", 1)
    type_list = GoodsType.objects.all()
    paginator = Paginator(type_list, 10)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request, 'store/goods_type_list.html', locals())
# 添加商品类别
def add_goods_type(request):
    if request.method == "POST":
        type_name = request.POST.get("type_name")
        type_description = request.POST.get("type_description")
        type_image = request.FILES.get("type_image")
        GoodsType.objects.create(
            type_name=type_name,
            type_description=type_description,
            type_picture=type_image
        )
    return HttpResponseRedirect("/store/goods_type_list/")
# 删除商品类别
def del_goodsType(request):
    referer = request.META.get("HTTP_REFERER")
    goods_type_id = request.GET.get("goods_type_id")
    GoodsType.objects.filter(id=goods_type_id).delete()
    return HttpResponseRedirect(referer)