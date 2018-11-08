from django.contrib.auth.backends import ModelBackend

from .models import MyUser


class MyBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            #使用用户名登录
            user = MyUser.objects.get(username=username)
        #Exception 异常
        except Exception:
            try:
                #使用邮箱登录
                user = MyUser.objects.get(email=username)
            except Exception as e:
                return None

        #密码验证
        if user.check_password(password):
            return user

        else:
            return None


