from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r"^home$",home,name="home"),
    url(r"^market$",market,name="market"),
    url(r"^cart$",cart,name="cart"),
    url(r"^mine$",mine,name="mine"),
    url(r"^market_with_params/(\d+)/(\d+)/(\d+)",
            market_with_params,
            name="market_params"
        ),

    url(r"^register$",RegisterAPI.as_view(),name="register"),

    url(r"^login$",LoginAPI.as_view(),name="login") ,  #登录
    url(r"^logout$",LogoutAPI.as_view(),name="logout"),  #退出
    url(r"^confrim/(.*)",confrim,name="confrim"),          #验证链接

    url(r"^check_uname$",check_uname,name="check_uname"),   #验证用户是否可用

    url(r"^cart_api$",CartAPI.as_view()),

    url(r"^cart_status$",CartStatusAPI.as_view()),   #商品选中状态


    url(r"^cart_all_status$",CartAllStatusAPI.as_view()),  #全选状态


    url(r"^cart_item$",CartItemAPI.as_view()),    #购物车加操作

    url(r"^order$",OrderAPI.as_view(),name="order"),          #订单
]