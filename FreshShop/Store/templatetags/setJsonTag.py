import json
from django import template
from Store import models

register = template.Library()

@register.filter(name="deserialization")
def Deserialization(value):
    return json.loads(value)

@register.filter(name="goodsOfstore")
def goodsOfstore(value):
    goods_id = int(value)
    goods = models.Goods.objects.get(id=goods_id)
    store = goods.store_id.all()
    return store

@register.filter(name="has_store")
def has_store(value):
    store = models.Store.objects.filter(user_id=value)
    if store:
        return True
    else:
        return False

@register.filter(name="goodsType")
def goodsType(value):
    goods_type = models.GoodsType.objects.get(id=value)
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
