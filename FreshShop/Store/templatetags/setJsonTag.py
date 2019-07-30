import json
from django import template
from Store import models as Sm
from Buyer import models as Bm

register = template.Library()

@register.filter(name="addData")
def addData(value, data):
    return value+data

@register.filter(name="lengthCart")
def lengthCart(value):
    cart_list = Bm.Cart.objects.filter(user_id=value)
    return len(cart_list)

@register.filter(name="getTotal")
def getTotal(value):
    total = 0
    for i in value:
        total += i.get("total")
    return total

@register.filter(name="deserialization")
def Deserialization(value):
    return json.loads(value)

@register.filter(name="goodsOfstore")
def goodsOfstore(value):
    goods_id = int(value)
    store = Sm.Store.objects.get(id=goods_id)
    return store.store_name

@register.filter(name="has_store")
def has_store(value):
    store = Sm.Store.objects.filter(user_id=value)
    if store:
        return True
    else:
        return False

@register.filter(name="goodsType")
def goodsType(value):
    goods_type = Sm.GoodsType.objects.get(id=value)
    return goods_type.type_name

@register.filter(name="goodsTypeList")
def goodsTypeList(value):
    result = []
    for type in value:
        goods_list = type.goods_set.filter(goods_status=1)
        if goods_list:
            result.append(type)
    return result

@register.filter(name="typeData")
def typeData(value):
    return value.goods_set.filter(goods_status=1)[:4]

@register.filter(name="lenCart")
def lenCart(value):
    return len(value)

@register.filter(name="goodsOfOrder")
def goodsOfOrder(value):
    goodslist = value.orderdetail_set.all()
    return goodslist

@register.filter(name="getPicture")
def getPicture(value):
    goods = Sm.Goods.objects.filter(id=value).first()
    return goods.goods_images
