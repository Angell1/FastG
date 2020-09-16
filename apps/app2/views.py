
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render,HttpResponse,redirect

class TestView(APIView):
    def dispatch(self, request, *args, **kwargs):
        """
        请求到来之后，都要执行dispatch方法，dispatch方法根据请求方式不同触发 get/post/put等方法

        注意：APIView中的dispatch方法有好多好多的功能
        """
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return Response('!!!!!!!!!!!!!!!!!!!!!!!!!!')

    def post(self, request, *args, **kwargs):
        return Response('POST请求，响应内容')
