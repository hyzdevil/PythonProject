from django.db import models

# Create your models here.

# 卖家
class Seller(models.Model):
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=32, verbose_name="密码")
    nickname = models.CharField(max_length=32, verbose_name="昵称", null=True, blank=True)
    phone = models.CharField(max_length=32, verbose_name="电话", null=True, blank=True)
    email = models.EmailField(verbose_name="邮箱", null=True, blank=True)
    address = models.CharField(max_length=300, verbose_name="地址", null=True, blank=True)
    picture = models.ImageField(upload_to="store/images", verbose_name="用户头像", null=True, blank=True)
    card_id = models.CharField(max_length=32, verbose_name="身份证", null=True, blank=True)

    def __str__(self):
        return self.username

# 店铺类型
class StoreType(models.Model):
    store_type = models.CharField(max_length=32, verbose_name="类型名称")
    type_description = models.TextField(max_length=32, verbose_name="类型描述")

# 店铺
class Store(models.Model):
    store_name = models.CharField(max_length=32, verbose_name="店铺名称")
    store_description = models.TextField(verbose_name="店铺描述")
    store_address = models.CharField(max_length=300, verbose_name="店铺地址")
    store_logo = models.ImageField(upload_to="store/images",verbose_name="店铺logo")
    store_phone = models.CharField(max_length=32, verbose_name="店铺电话")
    store_money = models.FloatField(verbose_name="店铺注册资金")

    user = models.ForeignKey(to=Seller, on_delete=models.CASCADE, verbose_name="店铺主人")
    type = models.ManyToManyField(to=StoreType, verbose_name="店铺类型")

# 商品类型
class GoodsType(models.Model):
    type_name = models.CharField(max_length=32, verbose_name="商品类别")
    type_picture = models.ImageField(upload_to="store/images", verbose_name="商品类别")
    type_description = models.TextField(verbose_name="类别描述")
    type_class = models.CharField(max_length=32, verbose_name="类别class", default=1)

# 商品
class Goods(models.Model):
    goods_name = models.CharField(max_length=32, verbose_name="商品名称")
    goods_price = models.FloatField(verbose_name="商品价格")
    goods_images = models.ImageField(upload_to="store/images",verbose_name="商品图片")
    goods_number = models.IntegerField(verbose_name="商品库存")
    goods_description = models.TextField(verbose_name="商品描述")
    goods_date = models.DateField(verbose_name="出厂日期")
    goods_safeDate = models.IntegerField(verbose_name="保质期")
    goods_status = models.IntegerField(verbose_name="商品状态", default=1)

    store_id = models.ForeignKey(to=Store, verbose_name="商品店铺", on_delete=models.CASCADE)
    goods_type = models.ForeignKey(to=GoodsType, on_delete=models.CASCADE)

# 商品图片
class Goods_img(models.Model):
    img = models.ImageField(upload_to="store/images", verbose_name="商品图片")
    img_description = models.TextField(verbose_name="图片描述")

    goods_id = models.ForeignKey(to=Goods, on_delete=models.CASCADE, verbose_name="商品id")

class Area(models.Model):
    atitle = models.CharField(max_length=30)
    aparent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.atitle