"""
后台页面
AUTH:
DATE:
"""
from django.contrib.auth.hashers import check_password,make_password
from django.core import serializers
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
import redis

from GoodBuy.settings import SESSION_REDIS
from app.models import AdminUser, Hot
from app.untils.wrapper_code import is_login

# 后台登录
def login(request):
    if request.method == 'GET':
        data = {'code':200}
        return render(request, 'admin/login.html',)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        v_code = request.POST.get('verify_code_text')
        data = {}
        if not all([username, password, v_code]):
            data['code'] = 1001
            data['msg'] = '参数错误'
            return render(request, 'admin/login.html', data)
        if v_code != request.session['v_code']:
            data['code'] = 1002
            data['msg'] = '验证码错误'
            return render(request, 'admin/login.html', data)
        try:
            user = AdminUser.objects.filter(username=username).first()
            if not check_password(password, user.password) and not user:
                data['code'] = 1003
                data['msg'] = '用户名或密码错误'
                return render(request, 'admin/login.html', data)
            request.session['admin_user_id'] = user.id
            data['code'] = 1003
            data['user_id'] = user.id
            return HttpResponseRedirect('/admin_page/index/')
        except Exception:
            data['code'] = 1004
            data['msg'] = '未知错误'
            return render(request,'admin/login.html',data)

@is_login
def admin_page(request):
    if request.method == 'GET':
        return render(request, 'admin/index.html')

@is_login
def admin_top(request):
    return render(request, 'admin/top.html')

@is_login
def admin_menu(request):
    return render(request, 'admin/menu.html')

@is_login
def admin_main(request):
    if request.method == 'GET':
        return render(request, 'admin/main.html')

@is_login
def admin_main_access(request):
    if request.method == 'GET':
        data = {}
        try:
            conn = redis.Redis(host=SESSION_REDIS['host'], port=SESSION_REDIS['port'], password=SESSION_REDIS['password'])
            access_dict = conn.hgetall('access')
            data['code'] = 200
            # 把一个字典的键和值全部转码
            access_list = list(map(lambda x: (x.decode('utf-8'), access_dict[x].decode('utf-8')), access_dict))
            # access_list.sort(key=lambda x: int(x[1]))
            access_amount = [i[1] for i in access_list]
            access_name = [i[0] for i in access_list]
            data['access_amount'] = access_amount
            data['access_name'] = access_name
            return JsonResponse(data)
        except Exception:
            data['code'] = 1101
            data['msg'] = '数据获取失败，请重新加载'
            return JsonResponse(data)

@is_login
def admin_main_hotword(request):
    if request.method == 'GET':
        data = {}
        try :
            hotwords = Hot.objects.filter().order_by('-count')[:6]
            hotwords_list = [{'value': i.count, 'name': i.word} for i in hotwords]
            data['code'] = 200
            data['hotwords'] = hotwords_list
            return JsonResponse(data)
        except Exception:
            data['code'] = 1301
            data['msg'] = '服务器不堪重负了'

        return JsonResponse(data)

#
@is_login
def logout(request):
    del request.session['admin_user_id']
    return HttpResponseRedirect('/admin_page/index/')
