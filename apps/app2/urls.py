from django.urls import path
from .views import GetWork,Getaddress,GetFirm,Getkind,IndexViewset,Frontindex



app_name = 'app2'
urlpatterns = [
    #主页
    path('index/',IndexViewset.as_view()),
    #前页
    path('frontindex/', Frontindex.as_view()),
    #
    path('work/',GetWork.as_view()),
    #岗位详情

    #
    path('address/',Getaddress.as_view()),
    #公司
    path('firm/',GetFirm.as_view()),
    #分类相关的统计
    path('kind/',Getkind.as_view()),

    
]