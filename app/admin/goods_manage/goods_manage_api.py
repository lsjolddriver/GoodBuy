"""
后台商品管理页面
AUTH:
DATE:
"""
from django.shortcuts import render
from django.http.response import HttpResponse


def goods_manage(request):
    return HttpResponse('Hello goods_manage')