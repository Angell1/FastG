from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

class UserProfile(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    phone = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    password = models.EmailField(max_length=100, null=True, blank=True, verbose_name="密码")
    # user_secret = models.UUIDField(default=uuid4(), verbose_name='用户JWT秘钥')
    # user_jwt = models.CharField(null=True, blank=True, max_length=1000, verbose_name="用户秘钥")
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.username


