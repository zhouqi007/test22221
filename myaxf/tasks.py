from celery import task
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template import loader

from django.core.cache import cache
from .my_util import *


#发送邮件


@task
def send_verify_email(url,user_id,receives):
    #发送邮件
    title = "注册成功"
    content = ""
    #加载页面
    template = loader.get_template("user/email.html")
    html = template.render({"url":url})
    email_from = settings.DEFAULT_FROM_EMAIL
    #发送邮件
    send_mail(title,content,email_from,[receives],html_message=html)

    print(user_id)
    #设置缓存
    cache.set(url.split("/")[-1],user_id,settings.VERIFY_CODE_MAX_AGE)



#验证成功跳转到登录页面