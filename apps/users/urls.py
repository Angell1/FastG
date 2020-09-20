
from django.urls import path,include
from users.views import Regis,Login,Logout,refresh_captcha

app_name = 'users'

urlpatterns = [
    #主页
    # 定义注册URL
    path(r'register/', Regis.as_view()),
    # 定义登录URL
    path(r'login/', Login.as_view()),
    # 定义注销URL
    path(r'logout/', Logout.as_view()),
    # 图片验证码
    path('captcha/', include('captcha.urls')),
    # 刷新验证码，ajax
    path('refresh_captcha/', refresh_captcha),

]