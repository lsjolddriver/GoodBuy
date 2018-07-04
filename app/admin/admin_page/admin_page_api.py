"""
后台页面
AUTH:
DATE:
"""
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, render_to_response
from django.http.response import HttpResponse, JsonResponse

from app.models import AdminUser


def login(request):
    if request.method == 'GET':
        return render(request, 'admin/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('username')
        v_code = request.POST.get('verify_code')
        data = {}
        if not all([username, password, v_code]):
            data['code'] = 1001
            data['msg'] = '参数错误'
            return JsonResponse(data)
        if v_code != request.session['v_code']:
            data['code'] = 1002
            data['msg'] = '验证码错误'
            return JsonResponse(data)
        try:
            user = AdminUser.objects.filter(username=username).first()
            if not check_password(password, user.password) and not user:
                data['code'] = 1003
                data['msg'] = '用户名或密码错误'
                return JsonResponse(data)
            request.session['user_id'] = user.id
            del request.session['']
            data['code'] = 1003
            data['user'] = user.id
            return JsonResponse(data)
        except Exception:
            data['code'] = 1004
            data['msg'] = '服务器挂了'
            return JsonResponse(data)

def admin_page(request):
    if request.method == 'GET':
        return render(request, 'admin/index.html')
    if request.method == 'POST':
        pass

def admin_top(request):
    return render(request, 'admin/top.html')

def admin_menu(request):
    return render(request, 'admin/menu.html')

def admin_main(request):
    return render(request, 'admin/main.html')

