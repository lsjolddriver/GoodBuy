"""
前台首页
AUTH:
DATE:
"""
from django.shortcuts import render
from django.http.response import HttpResponse


def hello_home_page(request):
    return HttpResponse('Hello Home Page')