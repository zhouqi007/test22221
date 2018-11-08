from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render, redirect
from django.core.cache import cache
# Create your views here.
from django.urls import reverse
from django.views import View
from .my_util import *
from .tasks import send_verify_email
from .models import *


def home(req):
    wheels = Wheel.objects.all()
    menus = Nav.objects.all()
    mustbuy = MustBuy.objects.all()
    shop = Shop.objects.all()
    mainshow = MainShow.objects.all()
    result = {
        "title":"首页",
        "wheels":wheels,
        "menus":menus,
        "mustbuy":mustbuy,
        "shop1":shop[0],
        "shop2": shop[1:3],
        "shop3":shop[3:7],
        "shop4":shop[7:11],
        "mainshow":mainshow,
    }
    return render(req,"home/home.html",result)

def market(req):
    return redirect(reverse("myaxf:market_params",args=("104749","0",0)))

def market_with_params(req,type_id,sub_type_id,order_type):
    #获取所有的一级分类
    types = FoodTypes.objects.all()

    #获取二级分类
    current_cate = types.filter(typeid=type_id)[0]
    childtypenames = current_cate.childtypenames.split("#")
    sub_types = [i.split(":") for i in childtypenames]

    #根据typeid搜索商品信息
    goods = Goods.objects.filter(
        categoryid=int(type_id)
    )

#根据二级分类的id查询数据
    if sub_type_id == "0":
        pass
    else:
        goods = goods.filter(childcid=int(sub_type_id))



#排序  0 不排序  1 按价格排序   2 按销量排序
    if int(order_type) == 0:
        pass
    elif int(order_type)  == 1:
        goods = goods.order_by("price")
    else:
        goods = goods.order_by("productnum")

    # 添加num属性
    # 知道用户购物车商品的对应的数量
    user = req.user
    if isinstance(user, MyUser):
        tmp_dict = {}
        # 去购物车查看数据
        cart_nums = Cart.objects.filter(user=user)
        for i in cart_nums:
            tmp_dict[i.goods.id] = i.num
        for i in goods:
            # 添加商品数量
            i.num = tmp_dict.get(i.id) if tmp_dict.get(i.id) else 0

    result = {
        "title": "闪购",
        "types": types,
        "goods":goods,
        "current_type_id":type_id,
        "sub_types":sub_types,
        "current_sub_type_id":sub_type_id,
        "order_type":int(order_type),
    }
    return render(req, "market/market.html", result)

@login_required(login_url="/myaxf/login")
def cart(req):
    #确定用户
    user = req.user
    #根据用户获得购物车数据
    data = Cart.objects.filter(user_id=user.id)

    #算钱
    sum_money = get_cart_money(data)
    #判断全选按钮的状态 (有购物车商品并且没有没有选中的商品)
    if data.exists() and not data.filter(is_selected=False).exists():
        is_all_select = True
    else:
        is_all_select = False

    result = {
        "title":"购物车",
        "uname":user.username,
        "phone":user.phone if user.phone else "暂无",
        "address":user.address if user.address else "暂无",
        "cart_items":data,
        "sum_money":sum_money,
        "is_all_select":is_all_select,
    }
    return render(req,"cart/cart.html",result)


def mine(req):
    #获取用户
    user = req.user
    #表示登录状态
    is_login = True

    # 判断是否为匿名用户，是否登录  AnonymousUser表示匿名用户
    if isinstance(user,AnonymousUser):
        is_login = False

    u_name = user.username if is_login else ""
    icon = "http://"+ req.get_host()+ "/static/uploads/" + user.icon.url if is_login else ""
    result = {
        "title":"我的",
        "is_login":is_login,
        "u_name":u_name,
        "icon":icon,
    }
    return render(req,"mine/mine.html",result)


#注册
class RegisterAPI(View):

    def get(self,req):
        return render(req,"user/register.html")


    def post(self,req):
        params = req.POST
        icon = req.FILES.get("u_icon")
        name = params.get("u_name")
        pwd = params.get("u_pwd")
        confrim_pwd = params.get("u_confrim_pwd")
        email = params.get("email")
        print(pwd)
        print(confrim_pwd)
        #校验密码
        if pwd and confrim_pwd and pwd == confrim_pwd:
            #判断用户名是否存在
            if MyUser.objects.filter(username=name).exists():
                return render(req,"user/register.html",{"help_msg":"该用户已存在"})

            else:
                user = MyUser.objects.create_user(
                    username=name,
                    password=pwd,
                    email=email,
                    icon=icon,
                    is_active=False
                )
                #生成验证链接
                url = "http://" + req.get_host() + "/myaxf/confrim/" + get_uuid_str()
                #发送邮件  异步调用
                send_verify_email.delay(url,user.id,email)
                #设置缓存  返回登录页面
                return render(req,"user/login.html")
        else:
            return render(req,"user/register.html",{"help_msg":"用户或密码错误"})

#验证邮件
def confrim(req,uuid_str):
    #缓存拿参数
    user_id = cache.get(uuid_str)

    #如果拿到用户id，就修改is_active字段
    if user_id:
        user = MyUser.objects.get(pk = int(user_id))
        user.is_active = True
        user.save()
        return redirect(reverse("myaxf:login"))
    #没有就返回验证失败
    else:
        return HttpResponse("<h2>链接失效</h2>")

class LoginAPI(View):
    def get(self,req):
        return render(req,"user/login.html")

    def post(self,req):
        # 解析参数
        params = req.POST
        name = params.get("name")
        pwd = params.get("pwd")
        print(name)
        print(pwd)
        #校验数据
        if not (name and pwd):
            data = {
                "code":2,
                "msg":"账号或密码不能为空",
                "data":""
            }
            return JsonResponse(data)

        user = authenticate(username = name,password = pwd)

        if user:
            login(req,user)
            data = {
                "code":1,
                "msg":"ok",
                "data":"/myaxf/mine"
            }
            # return render(req,"mine/mine.html")
            return JsonResponse(data)
        else:
            data = {
                "code": 3,
                "msg": "账号或密码错误",
                "data": ""
            }
            return JsonResponse(data)


class LogoutAPI(View):

    def get(self,req):
        logout(req)
        return redirect(reverse("myaxf:mine"))

#验证用户是否可用
def check_uname(req):
    params = req.GET
    uname = params.get("uname")
    #判断数据不能是空白，然后去搜索用户
    if uname and len(uname)>=3:
        if MyUser.objects.filter(username=uname).exists():
            data = {
                "code":1,
                "msg":"账号已存在",
                "data":""
            }

        else:
            data = {
                "code": 1,
                "msg": "账号可用",
                "data": ""
            }

    else:
        data = {
            "code": 1,
            "msg": "用户名过短",
            "data": ""
        }

    return JsonResponse(data)


#闪购数据的增减
class CartAPI(View):

    def post(self,req):
        #查看用户是否登录
        user = req.user
        if not isinstance(user,MyUser):
            data = {
                "code":2,
                "msg":"not_login",
                "data":"/myaxf/login"
            }
            return JsonResponse(data)

        # 拿参数
        op_type = req.POST.get("type")
        g_id = int(req.POST.get("g_id"))
        #先获取商品数据
        goods = Goods.objects.get(pk=g_id)
        #添加商品
        if op_type == "add":
            goods_num = 1
            #添加购物车操作
            #看库存
            if goods.storenums >1:
                #去购物车判断是否第一次加入
                cart_goods = Cart.objects.filter(user=user,goods=goods)
                if cart_goods.exists():
                    #不是第一次加
                    cart_item = cart_goods.first()
                    #在原来基础上加1
                    cart_item.num = cart_item.num + 1
                    cart_item.save()
                    #修改返回值
                    goods_num = cart_item.num
                else:
                    #第一次加入
                    Cart.objects.create(
                        user = user,
                        goods = goods
                    )
                data = {
                    "code":1,
                    "msg":"ok",
                    "data":goods_num
                }
                return JsonResponse(data)

            else:
                data = {
                    "code":3,
                    "msg":"库存不足",
                    "data":""
                }

                return JsonResponse(data)
            
            
        #减商品
        elif op_type == "sub":
            goods_num = 0
            #先去查购物车数据

            cart_item = Cart.objects.get(
                user=user,
                goods=goods
            )
            cart_item.num = cart_item.num - 1
            cart_item.save()
            if cart_item.num == 0:
                #如果等于零，删除数据
                cart_item.delete()
            else:
                goods_num = cart_item.num


            data = {
                "code":1,
                "msg":"ok",
                "data":goods_num
            }

            return JsonResponse(data)



class CartStatusAPI(View):

    def patch(self,req):
        params = QueryDict(req.body)
        c_id = int(params.get("c_id"))
        user = req.user
        #先拿到跟这个人有关的购物车
        cart_items = Cart.objects.filter(user_id=user.id)

        #拿到指定的拿一条数据
        cart_data = cart_items.get(id=c_id)

        #修改状态
        cart_data.is_selected = not cart_data.is_selected
        cart_data.save()

        #算钱
        sum_money = get_cart_money(cart_items)

        #判断是否全选
        if cart_items.filter(is_selected=False).exists():
            is_all_selected = False
        else:
            is_all_selected = True

        #返回数据
        data = {
            "code":1,
            "msg":"ok",
            "data":{
                "is_all_selected":is_all_selected,
                "sum_money":sum_money,
                "status":cart_data.is_selected,
            }
        }

        return JsonResponse(data)



class CartAllStatusAPI(View):
    def put(self,req):
        user = req.user
        #判断操作
        cart_items = Cart.objects.filter(user_id=user.id)
        is_all_select = False
        if cart_items.exists() and cart_items.filter(is_selected=False):
            is_all_select = True
        # 由于当前处于未全选的状态，我们需要将没有选择的状态取反
            cart_items.filter(is_selected=False).update(is_selected=True)

            sum_money = get_cart_money(cart_items)
        else:
            # 将所有选中的取反
            cart_items.update(is_selected = False)

            sum_money = 0

        # 返回数据
        result= {
            "code":1,
            "msg":"ok",
            "data":{
                "sum_money":sum_money,
                "all_select":is_all_select
            }
        }

        return JsonResponse(result)


#购物车加减
class CartItemAPI(View):

    def post(self,req):
        user = req.user
        c_id = req.POST.get("c_id")

        cart_item = Cart.objects.get(pk=int(c_id))
        # 检查库存
        if cart_item.goods.storenums<1:
            result = {
                "code":2,
                "msg":"库存不足",
                "data":""
            }
            return JsonResponse(result)

        cart_item.num += 1
        cart_item.save()
        cart_items = Cart.objects.filter(
            user_id=user.id,
            is_selected=True
        )
        sum_money = get_cart_money(cart_items)
        # 返回数据
        result = {
            "code":1,
            "msg":"ok",
            "data":{
                "num":cart_item.num,
                "sum_money":sum_money
            }
        }

        return JsonResponse(result)

    def delete(self,req):
        user = req.user
        c_id = int(QueryDict(req.body).get("c_id"))
        print(c_id)
        cart_item = Cart.objects.get(pk=c_id)
        cart_item.num -= 1
        cart_item.save()

        if cart_item.num == 0:
            goods_num = 0
            cart_item.delete()

        else:
            goods_num = cart_item.num


        cart_items = Cart.objects.filter(
            user_id=user.id,
            is_selected=True
        )

        sum_money = get_cart_money(cart_items)

        result = {
            "code":1,
            "msg":"ok",
            "data":{
                "num":goods_num,
                "sum_money":sum_money
            }
        }

        return JsonResponse(result)


# 下单
class OrderAPI(View):
    def get(self,req):
        user = req.user
        cart_items = Cart.objects.filter(
            user_id=user.id,
            is_selected=True
        )

        # 创建订单
        order = Order.objects.create(
            user=user
        )
        #向订单中添加数据
        for i in cart_items:
            OrderItem.objects.create(
                order=order,
                goods=i.goods,
                num = i.num,
                buy_money=i.goods.price
            )
        sum_money = get_cart_money(cart_items)
        # 清空购物车中的订单商品

        cart_items.delete()

        data = {
            "sum_money":sum_money,
            "order":order
        }

        return render(req,"order/order_detail.html",data)