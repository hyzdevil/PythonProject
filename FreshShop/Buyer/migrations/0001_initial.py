# Generated by Django 2.1.1 on 2019-07-29 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(verbose_name='收件地址')),
                ('port_num', models.CharField(max_length=32, verbose_name='邮编')),
                ('rece_phone', models.CharField(max_length=32, verbose_name='收件人电话')),
                ('rece_name', models.CharField(max_length=32, verbose_name='收件人')),
            ],
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=100, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('phone', models.CharField(blank=True, max_length=32, null=True, verbose_name='联系方式')),
                ('connect_adress', models.TextField(blank=True, null=True, verbose_name='联系地址')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=32, verbose_name='商品名称')),
                ('goods_id', models.IntegerField()),
                ('goods_price', models.FloatField()),
                ('goods_number', models.IntegerField()),
                ('goods_total', models.FloatField()),
                ('goods_picture', models.ImageField(upload_to='buyer/images')),
                ('isdelete', models.IntegerField(default=0)),
                ('store_id', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.Buyer')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=32, verbose_name='商品编号')),
                ('order_count', models.IntegerField(verbose_name='商品数量')),
                ('order_total', models.FloatField(verbose_name='商品总价')),
                ('order_status', models.IntegerField(choices=[(1, '未支付'), (2, '已支付'), (3, '已取消此订单')], default=1, verbose_name='订单状态')),
                ('order_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.Buyer', verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_id', models.IntegerField(verbose_name='商品ID')),
                ('goods_name', models.CharField(max_length=32, verbose_name='商品名称')),
                ('goods_price', models.FloatField(verbose_name='商品单价')),
                ('goods_number', models.IntegerField(verbose_name='商品购买数量')),
                ('goods_total', models.FloatField(verbose_name='商品总价')),
                ('goods_store', models.IntegerField(verbose_name='店铺ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.Order', verbose_name='订单ID')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.Buyer'),
        ),
    ]
