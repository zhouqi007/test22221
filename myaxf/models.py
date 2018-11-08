from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class MyUser(AbstractUser):
    email = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="邮箱"
    )
    address = models.CharField(
        max_length=251,
        verbose_name="地址",
        null=True
    )
    phone = models.CharField(
        max_length=13,
        verbose_name="手机号",
        null=True
    )

    icon = models.ImageField(
        upload_to="icons",
        null=True
    )

#抽象类
class BaseData(models.Model):
    img= models.CharField(
        max_length=251
    )
    name = models.CharField(
        max_length=40
    )
    trackid = models.CharField(
        max_length=30
    )
    class Meta:
        abstract=True

class Wheel(BaseData):

    class Meta:
        db_table = "axf_wheel"

class Nav(BaseData):

    class Meta:
        db_table = "axf_nav"

class MustBuy(BaseData):

    class Meta:
        db_table="axf_mustbuy"

class Shop(BaseData):

    class Meta:
        db_table="axf_shop"

class MainShow(BaseData):
    categoryid = models.CharField(
        max_length=50,
        null=True
    )
    brandname = models.CharField(
        max_length=30,
        null=True
    )
    img1 = models.CharField(
        max_length=251,
        null=True
    )
    childcid1 =models.CharField(
        max_length=50,
        null=True
    )
    productid1 = models.CharField(
        max_length=50,
        null=True
    )
    longname1 = models.CharField(
        max_length=50,
        null=True
    )
    price1 = models.CharField(
        max_length=50,
        null=True
    )
    marketprice1 = models.CharField(
        max_length=50,
        null=True
    )
    img2 = models.CharField(
        max_length=251,
        null=True
    )
    childcid2 = models.CharField(
        max_length=50,
        null=True
    )
    productid2 = models.CharField(
        max_length=50,
        null=True
    )
    longname2 = models.CharField(
        max_length=50,
        null=True
    )
    price2 = models.CharField(
        max_length=50,
        null=True
    )
    marketprice2 = models.CharField(
        max_length=50,
        null=True
    )
    img3 = models.CharField(
        max_length=251,
        null=True
    )
    childcid3 = models.CharField(
        max_length=50,
        null=True
    )
    productid3 = models.CharField(
        max_length=50,
        null=True
    )
    longname3 = models.CharField(
        max_length=50,
        null=True
    )
    price3 = models.CharField(
        max_length=50,
        null=True
    )
    marketprice3 = models.CharField(
        max_length=30,
        null=True
    )

    class Meta:
        db_table="axf_mainshow"


class FoodTypes(models.Model):
    typeid = models.CharField(
        max_length=20
    )
    typename = models.CharField(
        max_length=30
    )
    childtypenames = models.CharField(
        max_length=255
    )
    typesort = models.IntegerField()

    class Meta:
        db_table = "axf_foodtypes"


class Goods(models.Model):
    productid = models.CharField(
        max_length=20
    )
    productimg = models.CharField(
        max_length=255
    )
    productname = models.CharField(
        max_length=130
    )
    productlongname = models.CharField(
        max_length=190
    )
    isxf = models.BooleanField(
        default=0
    )
    pmdesc = models.IntegerField()
    specifics = models.CharField(
        max_length=40
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    marketprice = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    categoryid = models.IntegerField(

    )
    childcid = models.IntegerField()
    childcidname = models.CharField(
        max_length=30
    )
    dealerid = models.CharField(
        max_length=30
    )
    storenums = models.IntegerField(
        verbose_name="库存"
    )
    productnum = models.IntegerField(
        verbose_name="销量"
    )
    class Meta:
        db_table = "axf_goods"

#购物车
class Cart(models.Model):
    user = models.ForeignKey(
        MyUser
    )
    goods = models.ForeignKey(
        Goods
    )
    num = models.IntegerField(
        default=1
    )
    create_time = models.DateTimeField(
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        auto_now=True
    )
    is_selected = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = "购物车"
        index_together = ["user","goods"]


# 订单
class Order(models.Model):
    ORDER_STATUS = (
        (1,"未付款"),
        (2, "已付款"),
        (3, "已发货"),
        (4, "已收货"),
        (5, "待评价"),
        (6, "已评价"),
    )
    user = models.ForeignKey(
        MyUser
    )
    create_time = models.DateTimeField(
        auto_now_add=True
    )
    status = models.IntegerField(
        choices=ORDER_STATUS,
        default=1
    )

#订单详细数据
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order
    )
    goods = models.ForeignKey(
        Goods
    )
    num = models.IntegerField(
        verbose_name="数量"
    )
    buy_money = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
