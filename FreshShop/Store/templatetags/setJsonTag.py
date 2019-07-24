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