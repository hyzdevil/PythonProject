from django.db import models

from Store.models import Goods

# Create your models here.

ORDER_STATUS = (
    (1, "未支付"),
    (2, "已支付"),
    (3, "已取消此订单"),
)

class Buyer(models.Model):
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=100, verbose_name="密码")
    email = models.EmailField(verbose_name="邮箱")
    phone = models.CharField(max_length=32,verbose_name="联系方式",null=True,blank=True)
    connect_adress = models.TextField(verbose_name="联系地址",null=True,blank=True)

    def __str__(self):
        return self.username

class Cart(models.Model):
    goods_name = models.CharField(max_length=32, verbose_name="商品名称")
    goods_id = models.IntegerField()
    goods_price = models.FloatField()
    goods_number = models.IntegerField()
    goods_total = models.FloatField()
    goods_picture = models.ImageField(upload_to="buyer/images")
    isdelete = models.IntegerField(default=0)
    store_id = models.IntegerField()
    user = models.ForeignKey(to=Buyer, on_delete=models.CASCADE)

class Address(models.Model):
    address = models.TextField(verbose_name="收件地址")
    port_num = models.CharField(max_length=32, verbose_name="邮编")
    rece_phone = models.CharField(max_length=32, verbose_name="收件人电话")
    rece_name = models.CharField(max_length=32, verbose_name="收件人")

    user = models.ForeignKey(to=Buyer, on_delete=models.CASCADE)

class Order(models.Model):
    order_id = models.CharField(max_length=32, verbose_name="商品编号")
    order_count = models.IntegerField(verbose_name="商品数量")
    order_total = models.FloatField(verbose_name="商品总价")
    order_user = models.ForeignKey(to=Buyer, on_delete=models.CASCADE, verbose_name="用户")
    order_status = models.IntegerField(choices=ORDER_STATUS, default=1, verbose_name="订单状态")

class OrderDetail(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="订单ID")
    goods_id = models.IntegerField(verbose_name="商品ID")
    goods_name = models.CharField(max_length=32, verbose_name="商品名称")
    goods_price = models.FloatField(verbose_name="商品单价")
    goods_number = models.IntegerField(verbose_name="商品购买数量")
    goods_total = models.FloatField(verbose_name="商品总价")
    goods_store = models.IntegerField(verbose_name="店铺ID")