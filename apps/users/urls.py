
from django.urls import path
from .views import Regis,Login,Logout

app_name = 'users'

urlpatterns = [
    #主页
    # 定义注册URL
    path(r'register/', Regis.as_view()),
    # 定义登录URL
    path(r'login/', Login.as_view()),
    # 定义注销URL
    path(r'logout/', Logout.as_view()),


]