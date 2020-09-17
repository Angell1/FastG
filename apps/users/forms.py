from django import forms
from django.contrib.auth.models import User



class UserRegisterForm(forms.Form):
    """
    校验注册信息
    """
    username = forms.CharField(required=True, max_length=30, min_length=3,
                               error_messages={
                                   'required': '用户名必填',
                                   'max_length': '用户名不能超过30个字符',
                                   'min_length': '用户名不能少于3个字符'
                               })
    password = forms.CharField(required=True, min_length=6,
                               error_messages={
                                   'required': '密码必填',
                                   'min_length': '密码不能少于6个字符'
                               })
    password2 = forms.CharField(required=True, min_length=6,
                                error_messages={
                                    'required': '确认密码必填',
                                    'min_length': '确认密码不能少于6个字符'
                                })
    phone = forms.CharField(required=True, max_length=20,
                                error_messages={
                                    'required': '手机号必填',
                                    'max_length': '确认密码不能超过20个字符'
                                })
    email = forms.CharField(required=True, max_length=30,
                                error_messages={
                                    'required': '邮箱必填',
                                    'min_length': '确认密码不能超过30个字符'
                                })


class UserLoginForm(forms.Form):
    """
    校验登录信息
    """
    username = forms.CharField(required=True, max_length=30, min_length=3,
                               error_messages={
                                   'required': '用户名必填',
                                   'max_length': '用户名不能超过30个字符',
                                   'min_length': '用户名不能少于3个字符'
                               })
    password = forms.CharField(required=True, min_length=6,
                               error_messages={
                                   'required': '密码必填',
                                   'min_length': '密码不能少于6个字符'
                               })

