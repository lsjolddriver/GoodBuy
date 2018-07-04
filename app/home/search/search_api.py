"""
搜索页面
AUTH:
DATE:
"""
from django.shortcuts import render
from django.http.response import HttpResponse


def search(request):
    return HttpResponse('Hello world')