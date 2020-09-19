
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import auth
from .models import UserProfile
from .forms import UserRegisterForm, UserLoginForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend


#users.views中重写authenticate认证

class CustomBackend(ModelBackend):
   '''
   自定义用户验证(setting.py)
   '''
   def authenticate(self, request, username=None, password=None, **kwargs):
       try:
           user=UserProfile.objects.get(Q(username=username)|Q(mobile=username))
           if user.check_password(password):
                return user
       except Exception as e:
           return None


token_list = {"token1":"user1","token2":"user2"}

class TestAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        print(token)
        if token not in token_list:
            raise exceptions.AuthenticationFailed("用户认证失败")
        else:
            user = token_list[token]
        return (user, token)

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass




class Regis(APIView):
    #认证
    # authentication_classes = [TestAuthentication, ]
    def dispatch(self, request, *args, **kwargs):
        """
        请求到来之后，都要执行dispatch方法，dispatch方法根据请求方式不同触发 get/post/put等方法

        注意：APIView中的dispatch方法有好多好多的功能
        """
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        return render(request, 'users/test.html', locals())

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
                user = UserProfile()
                user.username = username
                user.set_password(password)
                user.phone = phone
                user.email = email
                user.save()
                # UserProfile.objects.create(username=username, password=password,phone = phone, email = email )
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
        print(request.POST.get('username'))
        print(request.POST.get('password'))
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user:
                # 用户名和密码是正确的,则登录
                auth.login(request, user)
                print(1)
                return redirect('http://127.0.0.1:8000/app2/frontindex/')
            else:
                # 密码不正确
                return render(request, 'users/login.html', locals(),{"status":"密码错误"})
        else:
            return render(request, 'users/login.html', locals(),{"status":"表单验证错误"})



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



