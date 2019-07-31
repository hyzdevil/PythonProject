import json
from django import template
from Store import models as Sm
from Buyer import models as Bm

register = template.Library()
# 数值相加
@register.filter(name="addData")
def addData(value, data):
    return value+data
# 返回当前用户的购物车的长度
@register.filter(name="lengthCart")
def lengthCart(value):
    cart_list = Bm.Cart.objects.filter(user_id=value)
    return len(cart_list)
# 返回订单的总价
@register.filter(name="getTotal")
def getTotal(value):
    total = 0
    for i in value:
        total += i.get("total")
    return total
# 对当前数据进行反序列化
@register.filter(name="deserialization")
def Deserialization(value):
    return json.loads(value)
# 获取当前商品所上架的店铺名称
@register.filter(name="goodsOfstore")
def goodsOfstore(value):
    goods_id = int(value)
    store = Sm.Store.objects.get(id=goods_id)
    return store.store_name
# 判断是否有店铺
@register.filter(name="has_store")
def has_store(value):
    store = Sm.Store.objects.filter(user_id=value)
    if store:
        return True
    else:
        return False
# 获取当前商品所属类型的名称
@register.filter(name="goodsType")
def goodsType(value):
    goods_type = Sm.GoodsType.objects.get(id=value)
    return goods_type.type_name
# 获取所有的拥有商品且是上架商品的类型列表
@register.filter(name="goodsTypeList")
def goodsTypeList(value):
    result = []
    for type in value:
        goods_list = type.goods_set.filter(goods_status=1)
        if goods_list:
            result.append(type)
    return result
# 获取当前类型的前4个商品
@register.filter(name="typeData")
def typeData(value):
    return value.goods_set.filter(goods_status=1)[:4]
# 获取购物车的大小
@register.filter(name="lenCart")
def lenCart(value):
    return len(value)
# 获取订单的所有商品
@register.filter(name="goodsOfOrder")
def goodsOfOrder(value):
    goodslist = value.orderdetail_set.all()
    return goodslist
# 获取图片地址
@register.filter(name="getPicture")
def getPicture(value):
    goods = Sm.Goods.objects.filter(id=value).first()
    return goods.goods_images
# 判断是否为空
@register.filter(name="isNone")
def isNone(value):
    if value is None:
        return "---------------------"
    else:
        return value
# 判断用户信息是否完整
@register.filter(name="userInfo")
def userInfo(valve):
    if valve.phone and valve.connect_adress:
        return False
    else:
        return True
# 订单时间
@register.filter(name="orderTime")
def orderTime(value):
    value = value[-14:]
    return value[:4]+"-"+value[4:6]+"-"+value[6:8]+" "+value[8:10]+":"+value[10:12]+":"+value[12:14]