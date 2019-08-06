import json
import time

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.shortcuts import HttpResponseRedirect

from Buyer.models import *
from Store.models import GoodsType
from Store.views import setPassword

from alipay import AliPay

# Create your views here.

def setOrderID(user_id):
    """
    设置订单编号
    时间+用户ID+商品ID+商铺ID
    """
    strtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return str(user_id)+strtime

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

def loginValid(fun):
    def inner(request, *args, **kwargs):
        c_name = request.COOKIES.get("username")
        s_name = request.session.get("username")
        if c_name and s_name:
            c_name = json.loads(c_name)
            user = Buyer.objects.filter(username=c_name).first()
            if user and user.username == s_name:
                return fun(request, *args, **kwargs)
        return HttpResponseRedirect("/buyer/login/")
    return inner

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
                request.session["is_login"] = True
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
    response.delete_cookie("cartlength")
    request.session.flush()
    return response

from django.views.decorators.cache import cache_page

@cache_page(60*15)
def goods_list(request):
    goodsLidt = []
    type_id = request.GET.get("type_id")
    goods_type = GoodsType.objects.filter(id = type_id).first()
    if goods_type:
        goodsLidt = goods_type.goods_set.filter(goods_status=1)
    return render(request, 'buyer/goods_list.html', {"goods_list":goodsLidt})

def goods_detail(request):
    goods_id = request.GET.get("goods_id")
    goods = Goods.objects.filter(id=goods_id).first()
    return render(request, 'buyer/goods_detail.html', {"goods":goods})

@loginValid
def cart(request):
    buyer_id = request.session.get("buyer_id")
    cart_list = Cart.objects.filter(user_id=buyer_id)
    return render(request, 'buyer/cart.html', locals())

def del_goods(request):
    cart_id = request.GET.get("cart_id")
    Cart.objects.filter(id=cart_id).delete()
    return HttpResponseRedirect("/buyer/cart/")

def add_cart(request):
    if request.session.get("is_login", None):
        buyer_id = request.session.get("buyer_id")
        goods_id = int(request.POST.get("goods_id"))
        goods_number = int(request.POST.get("number"))
        goods_total = float(request.POST.get("total"))
        goods = Goods.objects.filter(id=goods_id).first()
        cart = Cart()
        cart.goods_name = goods.goods_name
        cart.goods_id = goods.id
        cart.goods_price = goods.goods_price
        cart.goods_number = goods_number
        cart.goods_total = goods_total
        cart.goods_picture = goods.goods_images
        cart.store_id = goods.store_id_id
        cart.user_id = buyer_id
        cart.save()
        message = "成功添加到购物车"
        flag = 1
    else:
        message = "你还没有登录，请登录"
        flag = 0
    return JsonResponse({"message":message,"flag":flag})

@loginValid
def place_order(request):
    if request.method == "POST":
        content = []
        goods_id_list = request.POST.getlist("goods_id")
        num_list = request.POST.getlist("number")
        for (goods_id, num) in zip(goods_id_list, num_list):
            goods = Goods.objects.filter(id=int(goods_id)).first()
            data = {
                "goods":goods,
                "num":num,
                "total":int(num)*goods.goods_price,
            }
            content.append(data)
        return render(request, 'buyer/place_order.html',{"content":content})
    return render(request, 'buyer/place_order.html')

def add_order(request):
    user_id = request.session.get("buyer_id")
    order_list = Order.objects.filter(order_user_id=user_id)
    if request.method == "POST":
        number = request.POST.get("number")
        allTotal = request.POST.get("allTotal")
        goods_id_list = request.POST.getlist("goods_id")
        order = Order()
        order.order_id = setOrderID(user_id)
        order.order_count = len(goods_id_list)
        order.order_total = allTotal
        order.order_user_id = user_id
        order.save()
        for goods_id in goods_id_list:
            goods = Goods.objects.filter(id=goods_id).first()
            orderDetail = OrderDetail()
            orderDetail.order_id = Order.objects.get(order_id=setOrderID(user_id)).id
            orderDetail.goods_id = goods_id
            orderDetail.goods_name = goods.goods_name
            orderDetail.goods_price = goods.goods_price
            orderDetail.goods_number = number
            orderDetail.goods_total = int(number)*goods.goods_price
            orderDetail.goods_store = goods.store_id_id
            orderDetail.save()
        return HttpResponseRedirect("/buyer/user_order/")
    return render(request, 'buyer/user_order.html', {"order_list":order_list})

@loginValid
def user_order(request):
    user_id = request.session.get("buyer_id")
    order_list = Order.objects.filter(order_user_id=user_id)
    return render(request, 'buyer/user_order.html', locals())

@loginValid
def user_center(request):
    buyer_id = request.session.get("buyer_id")
    buyer = Buyer.objects.get(id=buyer_id)
    if request.method == "POST":
        phone = request.POST.get("phone")
        province_id = request.POST.get('province')
        city_id = request.POST.get('city')
        district_id = request.POST.get('district')
        province = Area.objects.get(id=province_id)
        city = Area.objects.get(id=city_id)
        district = Area.objects.get(id=district_id)
        detail = request.POST.get('detail')
        user_address = str(province) + str(city) + str(district) + str(detail)
        buyer.phone = phone
        buyer.connect_adress = user_address
        buyer.save()
        return HttpResponseRedirect("/buyer/user_center/")
    return render(request, 'buyer/user_center.html', locals())

def user_site(request):
    buyer_id = request.session.get("buyer_id")
    address_list = Address.objects.filter(user_id=buyer_id)
    if request.method == "POST":
        rece_name = request.POST.get("rece_name")
        port_num = request.POST.get("port_num")
        rece_phone = request.POST.get("rece_phone")
        province_id = request.POST.get('province')
        city_id = request.POST.get('city')
        district_id = request.POST.get('district')
        province = Area.objects.get(id=province_id)
        city = Area.objects.get(id=city_id)
        district = Area.objects.get(id=district_id)
        detail = request.POST.get('detail')
        rece_address = str(province) + str(city) + str(district) + str(detail)
        Address.objects.create(
            address=rece_address,
            port_num=port_num,
            rece_phone=rece_phone,
            rece_name=rece_name,
            user_id=buyer_id
        )
        return HttpResponseRedirect("/buyer/user_site/")
    return render(request, 'buyer/user_site.html', locals())

def pay_result(request):
    """
    charset=utf-8
    out_trade_no=10002
    method=alipay.trade.page.pay.return
    total_amount=1000.00
    sign=hVq%2FAkn889sf6b1%2FIGHews0zPnU%2FOexqL9aBGaBXaGxzl19dSJnUr3QMpuX4a%2BZg0gP%2FpQ%2BqTTmbfZY%2F6x1HobwqtClw0ymEumENNPR9ypJjsz6luSU0YVgp8nRXMU%2FiLWeIgIOY9yi4vF%2Fp5g3W%2FlsilsDkW9WkI1rXPQClrJ%2F3M4S7I1arZOg%2BHrmXu0TOGdmOC%2FM6mrgCGVPrcTGTCvgYcMW5r6JBJ%2BxkCENk%2BHdJ6IlLii3xQxZ5pHIcFUF%2FAY0MSWJ7%2Bh%2FPnwKbuzlx1e4cyUCHwG%2Bz49esnS%2FBseFLZTuK%2BtJxvGGlxzUZ%2FNVU6c4J0RK0Onvb7dF%2FU0A%2BNQ%3D%3D
    trade_no=2019072622001417201000054119
    auth_app_id=2016101000652485
    version=1.0
    app_id=2016101000652485
    sign_type=RSA2
    seller_id=2088102178922262
    timestamp=2019-07-26+18%3A23%3A26
    """
    order_id = request.GET.get("out_trade_no")
    order = Order.objects.get(order_id = order_id)
    order.order_status = 2
    order.save()
    return HttpResponseRedirect("/buyer/user_order/")

def pay_order(request):
    money = request.GET.get("money")
    order_id = request.GET.get("order_id")

    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqTcqSftTUVjRG/6Nr94zB3M1Ni/Pk65OcuvAQzcmfGSmB4xe1IPPIoFeB0dX4HRFd3fSUle9qwrapjk9d+MpYUFswXX4KX5gFz9BoO9iZclRNhdndgnqDYHo6gPtTh/UFsaWjthZFMwsZzp2JwMd2x5x6z7hwmYR6eZVC6Q1ZBmJrpXjUGRdXbrQQb3MNPWP3e3iVa6pK41TWMPMXqXghitoRAaReWopz4qTWCQpRFr4MGd0HMY62Mg8nhBQcdeWmAk6I9fVFjJeiwhSaINFJhVf7I0bAnCi6fOY1szN2EERRe+8wu0xluM3YQjMTJbjjspzqL821IXrYj+0uuT1uQIDAQAB
    -----END PUBLIC KEY-----"""

    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
    MIIEowIBAAKCAQEAqTcqSftTUVjRG/6Nr94zB3M1Ni/Pk65OcuvAQzcmfGSmB4xe1IPPIoFeB0dX4HRFd3fSUle9qwrapjk9d+MpYUFswXX4KX5gFz9BoO9iZclRNhdndgnqDYHo6gPtTh/UFsaWjthZFMwsZzp2JwMd2x5x6z7hwmYR6eZVC6Q1ZBmJrpXjUGRdXbrQQb3MNPWP3e3iVa6pK41TWMPMXqXghitoRAaReWopz4qTWCQpRFr4MGd0HMY62Mg8nhBQcdeWmAk6I9fVFjJeiwhSaINFJhVf7I0bAnCi6fOY1szN2EERRe+8wu0xluM3YQjMTJbjjspzqL821IXrYj+0uuT1uQIDAQABAoIBAQClKWoGYd+V06nuuAvVb3zBNcrnQ81IqOZ7Nu4m7QqMebSwQ2s/5BNl6306f4EfXH19OR+5LVi8PNDjU5VSkg+OlMwxHBMHdQkXR6+oBF83WEMDF97tEIo5euY6m3ChQ2HAhT7o1/RC33Iro501QM6AU/v/EBZMp1GuyhmSTkmqk8hIYCEBXDFezHiQcoCHFFto4aB2BjMeGBTlijEMIW8U75RjNXLmD9OiXaj26zptdV6l1vSJO7k63wzcBdHK3Ym3mHTuNMt0/nVSlv3brnmoPN8HWieaGhQYxd2Vrol7lKRXIcTh710TuURozmAXbftFIddoounK6Yjns3651MWBAoGBANEHy5DmuVTDbKboVlIYwzbWP+Snigov0y4EUc+3TLjf3uJl8mYMA/YKFWkCgWjQElUEhf08tIinnsZMQfZ5m8SUrN0V/7Q0zuc94bzIUatiwfDGPzJlYG+gu3Z1zPnDn06oNzqwKTJs+/lPFF/VQlxHTE4iyu2hjXLdh3lRjk0RAoGBAM89EO/S8AWygaWImavE+N9HPHyu4XtaDQxxSrJCD+Z3bZg84VzuSnDuGfkYRXZYY+INDe4GIbftud+scCXJu3zkiD53uE4tN0o743jaK5ml6Jwq/nfGOc0Ny/oizojMHCfYXtuZxCgh6OgjNWK2wS17Asjo2x+M4jZHgq/PaL4pAoGAJaR7ujpygZs3w87vTJV9AjEPDIRHTZJTO2Q3v2pI/LoED01Am7PqOrKSLHjxCQj/ZCQOZQ47jKhy5U7ySgqYTIxhnObLR46C/A2eyzpfyrdcKZnp449yEGgnmiuYoBnkZGvSllUG9je+IKVnC+MBslB8o02MscJ4EIloTiars6ECgYAcGIZUTT+3NgU3oPZcgD7RXoIH0VnGdGXyeuWKl0Q6lZRpIE/ZXoD/IHiq+axpKACao/RwgapOmk8p0OH/bYMaoo0KEwcMqjqluMrVFpb0pLaNfZK0QE6TyzwNNGzVxP5INKBfm1AptLczyZoyQN6dwOCWxmL2uw3sF/PSzAbCSQKBgGju4PO2DdcicCDfQLyUA2BNkNiJ7+idJfqJ8lQ0BYPZVUTSysRu50tdnU7KPS1kTzeHqkr8UFd2ynr4zqxUCWXSWJkHV4G/eYKcukpC39QqxChOXJhQX2iAL04x1qOnBD6JWdsMzjPhGbZeDfvoHFAZl4WoOZky2u0wy0p/yfTu
    -----END RSA PRIVATE KEY-----"""

    alipay = AliPay(
        appid="2016101000652485",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2"
    )

    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=str(money),
        subject="生鲜交易",
        return_url="http://127.0.0.1:8000/buyer/pay_result/",
        notify_url="http://127.0.0.1:8000/buyer/pay_result/"
    )

    return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?" + order_string)