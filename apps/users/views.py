import json,base64
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import auth
from django.contrib.auth import get_user_model
from users.forms import UserRegisterForm, UserLoginForm
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from rest_framework import exceptions
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
# from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from captcha.views import CaptchaStore, captcha_image
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer, RefreshJSONWebTokenSerializer,
    VerifyJSONWebTokenSerializer
)
from toolkit.test.userstoreimg import store_userimg,get_userimg
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication
from rest_framework_jwt.views import (
JSONWebTokenAPIView
)
from rest_framework_jwt.utils import jwt_decode_handler
User = get_user_model()

#users.views中重写authenticate认证

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, verification_code=None, hashkey=None, **kwargs):
        print("验证用户名，密码、验证码：")
        print(verification_code,hashkey)
        hashkey_response = CaptchaStore.objects.filter(hashkey=hashkey).first().response
        print(hashkey_response)
        if verification_code.lower() != hashkey_response:
            raise exceptions.AuthenticationFailed({"code": -1, "message": "验证码错误"})
        print('这个hashkey的文本为:', hashkey_response)
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print("账号不正确", e)
            raise exceptions.AuthenticationFailed({"code": -1, "message": "请检查账号是否正确"})

        try:
            if user.check_password(password):
                return user
            else:
                raise exceptions.AuthenticationFailed({"code": -1, "message": "请检查密码是否正确1"})
        except Exception as e:
            raise exceptions.AuthenticationFailed({"code": -1, "message": "请检查密码是否正确2"})


# 创建验证码
def create_captcha(request):
    hashkey = CaptchaStore.generate_key()  # 生成hashkey
    imgage = captcha_image(request, hashkey)
    # 将图片转换为base64
    image_base = base64.b64encode(imgage.content)
    print(hashkey)
    captcha = {'hashkey': hashkey, 'image_url': image_base.decode('utf-8')}
    return captcha

#刷新验证码
def refresh_captcha(request):
    return HttpResponse(json.dumps(create_captcha(request)), content_type='application/json')

# 验证验证码
# def jarge_captcha(captchaStr, captchaHashkey):
#     if captchaStr and captchaHashkey:
#         try:
#             # 获取根据hashkey获取数据库中的response值
#             get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
#             if get_captcha.response == captchaStr.lower():  # 如果验证码匹配
#                 return True
#         except:
#             return False
#     else:
#         return False



class Regis(APIView):
    #认证
    def dispatch(self, request, *args, **kwargs):
        """
        请求到来之后，都要执行dispatch方法，dispatch方法根据请求方式不同触发 get/post/put等方法

        注意：APIView中的dispatch方法有好多好多的功能
        """
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        return render(request, 'users/register.html', locals())

    def post(self, request, *args, **kwargs):
        print(request.POST.get('username'))
        print(request.POST.get('password'))
        print(request.POST.get('password2'))
        print(request.POST.get('phone'))
        print(request.POST.get('email'))
        # 校验页面中传递的参数，是否填写完整
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            # 获取校验后的用户名和密码
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            if len(User.objects.filter(username= username,password=password)) == 0:
                user = User()
                user.username = username
                user.set_password(password)
                user.phone = phone
                user.email = email
                user.save()
                store_userimg(user.id)
                # 实现跳转
                return HttpResponseRedirect('/users/login/')
            return render(request, 'users/register.html', locals())
        else:
            print('验证失败', form.errors)
            return render(request, 'users/register.html', locals())


class Login(JSONWebTokenAPIView):
    #验证用户并返回token
    serializer_class = JSONWebTokenSerializer
    def dispatch(self, request, *args, **kwargs):
        """
        请求到来之后，都要执行dispatch方法，dispatch方法根据请求方式不同触发 get/post/put等方法

        注意：APIView中的dispatch方法有好多好多的功能
        """
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        captcha = create_captcha(request)
        return render(request, 'users/login.html',locals())

    # def post(self, request, *args, **kwargs):
    #     return HttpResponseRedirect('/app2/index/')

class Logout(APIView):
    def dispatch(self, request, *args, **kwargs):
        """
        请求到来之后，都要执行dispatch方法，dispatch方法根据请求方式不同触发 get/post/put等方法

        注意：APIView中的dispatch方法有好多好多的功能
        """
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect(reverse('user:login'))

    def post(self, request, *args, **kwargs):
        return Response('POST请求，响应内容')



