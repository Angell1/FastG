from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import auth
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserRegisterForm, UserLoginForm
from django.http import HttpResponseRedirect
from django.urls import reverse
import time
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
# Create your views here.


class Regis(APIView):
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
            if len(UserProfile.objects.filter(username= username,password=password)) == 0:
                UserProfile.objects.create(username=username, password=password,phone = phone, email = email )
                # 实现跳转
                return  render(request, 'users/login.html')
            return render(request, 'users/register.html', locals())
        else:
            print('验证失败', form.errors)
            return render(request, 'users/register.html', locals())


class Login(APIView):
    def dispatch(self, request, *args, **kwargs):
        """
        请求到来之后，都要执行dispatch方法，dispatch方法根据请求方式不同触发 get/post/put等方法

        注意：APIView中的dispatch方法有好多好多的功能
        """
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        return render(request, 'users/login.html')

    def post(self, request, *args, **kwargs):
        # 表单验证，用户名和密码是否填写，校验用户名是否注册
        # print(request.POST.get('username'))
        # print(request.POST.get('password'))
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = None
            try:
                user = UserProfile.objects.filter(username= form.cleaned_data['username']).values_list("password")
            except Exception as  e:
                print("错误：匹配不到用户")
            if len(user):
                if user[0][0] == form.cleaned_data['password']:
                    return Response(str(user))
                else:
                    #重新登录
                    return render(request, 'users/login.html', locals(),{"status":"密码错误"})
            else:
                #注册
                return render(request, 'users/register.html', locals(),{'status':'用户不存在'})
        else:
            return render(request, 'users/login.html', locals())


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



