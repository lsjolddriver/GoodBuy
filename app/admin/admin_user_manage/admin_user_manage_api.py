"""
管理员账户管理页面
AUTH:
DATE:
"""
from django.shortcuts import render
from django.http.response import HttpResponse


def admin_user_manage(request):
    return HttpResponse('Hello world')