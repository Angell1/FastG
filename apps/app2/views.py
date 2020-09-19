import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render,HttpResponse,redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication
from rest_framework import mixins,viewsets
from rest_framework_jwt.utils import jwt_decode_handler

class CustomPaginator(Paginator):
    def __init__(self, current_page, max_pager_num, *args, **kwargs):
        """
        :param current_page: 当前页
        :param max_pager_num:最多显示的页码个数
        :param args:
        :param kwargs:
        :return:
        """
        self.current_page = int(current_page)
        self.max_pager_num = max_pager_num
        super(CustomPaginator, self).__init__(*args, **kwargs)

    def page_num_range(self):
        # 当前页面
        # self.current_page
        # 总页数
        # self.num_pages
        # 最多显示的页码个数
        # self.max_pager_num
        if self.num_pages < self.max_pager_num:
            return range(1, self.num_pages + 1)
        part = int(self.max_pager_num / 2)
        if self.current_page - part < 1:
            return range(1, self.max_pager_num + 1)
        if self.current_page + part > self.num_pages:
            return range(self.num_pages + 1 - self.max_pager_num, self.num_pages + 1)
        return range(self.current_page - part, self.current_page + part + 1)

def read():
    global df,dic
    id =0
    with open("C:\\FastG\\toolkit\\spaiderpkg\\olddata",mode="r+",encoding="utf-8") as f:
        for line in f.readlines():
             line = line.rstrip("\n").lstrip(" ")
             list = line.split(" ")
             date = {'ID':id,'分类': list[0], '岗位': list[1], '公司':list[2], '地址':list[3], '薪资':list[4],'URL':list[5],'存储时间':list[6]}  # 添加的一行数据
             s = pd.Series(date)
             s.name = id
             df = df.append(s)  # 添加
             id +=1
             if list[2] not in  dic:
                 dic[list[2]] = 1
             else:
                 dic[list[2]] += 1


df = pd.DataFrame(columns=['ID', '分类', '岗位', '公司', '地址', '薪资', 'URL', '存储时间'])
dic = {}
read()


# 首页
class IndexViewset(APIView):

    authentication_classes = (JSONWebTokenAuthentication)
    # def dispatch(self, request, *args, **kwargs):
    #     """
    #     请求到来之后，都要执行dispatch方法，dispatch方法根据请求方式不同触发 get/post/put等方法
    #
    #     注意：APIView中的dispatch方法有好多好多的功能
    #     """
    #     return super().dispatch(request, *args, **kwargs)
    #
    def get(self, request, *args, **kwargs):

        return render(request, 'app2/frontindex.html')

    def post(self, request, *args, **kwargs):
        return Response('POST请求，响应内容')

# 主页面
class Frontindex(APIView):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    def dispatch(self, request, *args, **kwargs):
        """
        请求到来之后，都要执行dispatch方法，dispatch方法根据请求方式不同触发 get/post/put等方法

        注意：APIView中的dispatch方法有好多好多的功能
        """
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print("验证后的token：",bytes.decode(request.auth))
        token_user = jwt_decode_handler(bytes.decode(request.auth))
        print(token_user['user_id'])
        current_page = request.GET.get("p",0)
        current_page = int(current_page)  # 字符--〉数字
        listdata = []
        length = len(df)
        for i in range(length):
            listdata.append(df.iloc[i])
        paginator = CustomPaginator(current_page, 11, listdata, 10)
        # per_page: 每页显示条目数量
        # count:    数据总个数
        # num_pages:总页数
        # page_range:总页数的索引范围，如: (1,10),(1,200)
        # page:     page对象
        try:
            posts = paginator.page(current_page)
            # has_next              是否有下一页
            # next_page_number      下一页页码
            # has_previous          是否有上一页
            # previous_page_number  上一页页码
            # object_list           分页之后的数据列表
            # number                当前页
            # paginator             paginator对象
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        # print(posts.object_list)
        return render(request, 'app2/index1.html', locals())

    def post(self, request, *args, **kwargs):
        return Response('POST请求，响应内容')



# 独立搜索
class GetWork(APIView):
    def dispatch(self, request, *args, **kwargs):
        """
        请求到来之后，都要执行dispatch方法，dispatch方法根据请求方式不同触发 get/post/put等方法

        注意：APIView中的dispatch方法有好多好多的功能
        """
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        workename = request.GET.get("workename", "")
        print(workename)
        current_page = request.GET.get("p",0)
        print(current_page)
        listdata = []
        if workename:
            listdata = []
            d1 = df[df['岗位'] == workename]
            for i in range(len(d1)):
                listdata.append(d1.iloc[i])
        print(listdata)
        paginator = CustomPaginator(current_page, 11, listdata, 10)
        try:
            posts = paginator.page(current_page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return render(request, 'app2/index1.html', locals())


    def post(self, request, *args, **kwargs):
        return Response('POST请求，响应内容')

# 公司页面
class GetFirm(APIView):
    def dispatch(self, request, *args, **kwargs):
        """
        请求到来之后，都要执行dispatch方法，dispatch方法根据请求方式不同触发 get/post/put等方法

        注意：APIView中的dispatch方法有好多好多的功能
        """
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        current_page = request.GET.get("p", 0)
        print(current_page)

        listdata = []
        for i in dic:
            jsondata = {"company": "", "count": "", "address":"", "level":""}
            jsondata["company"] = i
            jsondata["count"] = dic[i]
            listdata.append(jsondata)
        print(listdata)
        paginator = CustomPaginator(current_page, 11, listdata, 20)
        try:
            posts = paginator.page(current_page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        print(posts.object_list)
        return render(request, 'app2/firm1.html', locals())
    def post(self, request, *args, **kwargs):
        return Response('POST请求，响应内容')



class Getaddress(APIView):
    def dispatch(self, request, *args, **kwargs):
        """
        请求到来之后，都要执行dispatch方法，dispatch方法根据请求方式不同触发 get/post/put等方法

        注意：APIView中的dispatch方法有好多好多的功能
        """
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        address = request.GET.get("addressname", "")
        current_page = request.GET.get("p", 0)
        print(current_page)
        listdata = []
        if address:
            listdata = []
            d1 = df[df['地址'] == address]
            for i in range(len(d1)):
                listdata.append(d1.iloc[i])
        paginator = CustomPaginator(current_page, 11, listdata, 10)
        try:
            posts = paginator.page(current_page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return render(request, 'app2/index.html', locals())

    def post(self, request, *args, **kwargs):
        return Response('POST请求，响应内容')




class Getkind(APIView):
    def dispatch(self, request, *args, **kwargs):
        """
        请求到来之后，都要执行dispatch方法，dispatch方法根据请求方式不同触发 get/post/put等方法

        注意：APIView中的dispatch方法有好多好多的功能
        """
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        kind = request.GET.get("kind", "")
        current_page = request.GET.get("p", 0)
        print(current_page)
        listdata = []
        if kind:
            listdata = []
            d1 = df[df['分类'] == kind]
            for i in range(len(d1)):
                listdata.append(d1.iloc[i])
        paginator = CustomPaginator(current_page, 11, listdata, 10)
        try:
            posts = paginator.page(current_page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return render(request, 'app2/index.html', locals())
    def post(self, request, *args, **kwargs):
        return Response('POST请求，响应内容')

