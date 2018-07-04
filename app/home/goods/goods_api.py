"""
商品详情页面
AUTH:
DATE:
"""
from django.shortcuts import render
from django.http.response import HttpResponse


def goods(request):
    return HttpResponse('Hello goods')