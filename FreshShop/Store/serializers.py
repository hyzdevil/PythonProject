from rest_framework import serializers
from Store.models import *

class GoodsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Goods
        fields = ['goods_name', 'goods_price', 'goods_number', 'goods_description', 'id', 'goods_date', 'goods_safeDate', 'goods_type_id', 'store_id_id']

class GoodsTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoodsType
        fields = ['type_name', 'type_description']