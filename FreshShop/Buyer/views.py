import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.shortcuts import HttpResponseRedirect

from Buyer.models import *
from Store.models import *
from Store.views import setPassword

from alipay import AliPay

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
                response.set_cookie("cartlength", len(Cart.objects.filter(user_id=buyer.id)))
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
        cart.store_id = goods.store_id.all().first().id
        cart.user_id = buyer_id
        cart.save()
        message = "成功添加到购物车"
        flag = 1
    else:
        message = "你还没有登录，请登录"
        flag = 0
    return JsonResponse({"message":message,"flag":flag})

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
    return render(request, 'buyer/pay_result.html', locals())

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