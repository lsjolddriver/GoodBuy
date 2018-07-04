"""
后台页面
AUTH:
DATE:
"""
from django.shortcuts import render
from django.http.response import HttpResponse


def hello_admin_page(request):
    return HttpResponse('Hello world')