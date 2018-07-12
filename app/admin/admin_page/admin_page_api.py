"""
后台页面
AUTH: jason
DATE: 2018.07.07
"""
from django.contrib.auth.hashers import check_password
from django.core import serializers
from django.db.models import Count
from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponseRedirect
import redis
from django.views.decorators.http import require_GET, require_http_methods

from GoodBuy.settings import SESSION_REDIS
from app.models import AdminUser, Hot, Focus
from app.untils.wrapper_code import is_login

# 后台登录
@require_http_methods(['GET','POST'])
def login(request):
    if request.method == 'GET':
        return render(request, 'admin/login.html')
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
            if not user:
                data['code'] = 1003
                data['msg'] = '账号不存在'
                return render(request, 'admin/login.html', data)
            if  not check_password(password, user.password):
                data['code'] = 1004
                data['msg'] = '密码错误'
                return render(request, 'admin/login.html', data)
            request.session['admin_user_name'] = user.username
            data['code'] = 200
            data['user_id'] = user.id
            return HttpResponseRedirect('/admin_page/index/')
        except Exception:
            data['code'] = 1005
            data['msg'] = '未知错误'
            return render(request,'admin/login.html',data)

# 后台首页
@is_login
@require_GET
def admin_page(request):
    return render(request, 'admin/index.html')

# 后台头部
@is_login
@require_GET
def admin_top(request):
    return render(request, 'admin/top.html',
                  {'admin_user_name':request.session['admin_user_name']})

# 后台左边菜单
@is_login
@require_GET
def admin_menu(request):
    return render(request, 'admin/menu.html')

# 后台右边内容
@is_login
@require_GET
def admin_main(request):
    return render(request, 'admin/main.html')

# 各页面访问量统计
@is_login
@require_GET
def admin_main_access(request):
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

# 各时间段访问量统计
@is_login
@require_GET
def admin_main_access2(request):
    data = {}
    try:
        conn = redis.Redis(host=SESSION_REDIS['host'], port=SESSION_REDIS['port'], password=SESSION_REDIS['password'])

    except Exception:
        data['code'] = 1501
        data['msg'] = '数据获取失败，请重新加载'
        return JsonResponse(data)


# 热门对比词汇统计
@is_login
@require_GET
def admin_main_hotword(request):
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

# 收藏商品统计
@is_login
@require_GET
def admin_focus_goods(request):
    data = {}
    try:
        focus = Focus.objects.filter()
        all_focus_goods = focus.annotate(sum=Count('goods_id')).values('goods_id','sum','goods__name')
        focus_goods = list(all_focus_goods.order_by('-sum')[:6])
        data['code'] = 200
        data['focus'] = focus_goods
        return JsonResponse(data)
    except Exception:
        data['code'] = 1401
        data['msg'] = '服务器加载失败'

# 退出登录
@require_GET
def logout(request):
    del request.session['admin_user_name']
    return HttpResponseRedirect('/admin_page/index/')

