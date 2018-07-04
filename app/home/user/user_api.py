"""
用户
AUTH:
DATE:
"""
from django.shortcuts import render
from django.http.response import HttpResponse

def register(request):
    return HttpResponse('Hello world')


def login(request):
    return HttpResponse('Hello world')


def logout(request):
    return HttpResponse('Hello world')

