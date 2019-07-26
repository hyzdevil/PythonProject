from django.db import models

# Create your models here.

class Buyer(models.Model):
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=100, verbose_name="密码")
    email = models.EmailField(verbose_name="邮箱")
    phone = models.CharField(max_length=32,verbose_name="联系方式",null=True,blank=True)
    connect_adress = models.TextField(verbose_name="联系地址",null=True,blank=True)

    def __str__(self):
        return self.username

class Address(models.Model):
    address = models.TextField(verbose_name="收件地址")
    port_num = models.CharField(max_length=32, verbose_name="邮编")
    rece_phone = models.CharField(max_length=32, verbose_name="收件人电话")
    rece_name = models.CharField(max_length=32, verbose_name="收件人")

    user = models.ForeignKey(to=Buyer, on_delete=models.CASCADE)