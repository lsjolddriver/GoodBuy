"""
用户
AUTH:
DATE:
"""
import re
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

from app.models import UserTicket, User, Focus, Comments
from app.untils.functions import get_ticket, get_user


def user_register(request):
    if request.method == 'GET':
        return render(request, 'home/user/register.html')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        code = request.POST.get('checkcode')

        if not all([username, password, password2, code]):
            msg = '参数不能为空'
            return render(request, 'home/user/register.html', {'msg': msg})

        if password != password2:
            msg = '两次密码不一致'
            return render(request, 'home/user/register.html', {'msg': msg})

        if code != request.session['v_code']:
            msg = '验证码错误'
            return render(request, 'home/user/register.html', {'msg': msg})

        if User.objects.filter(username=username).first():
            msg = '用户名已被注册'
            return render(request, 'home/user/register.html', {'msg': msg})

        hash_password = make_password(password)
        User.objects.create(username=username,
                            password=hash_password,
                            )
        return HttpResponseRedirect('/user/user_login/')


def user_login(request):
    if request.method == 'GET':
        return render(request, 'home/user/login.html')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('checkcode')
        # 验证用户是否存在
        user = User.objects.filter(username=username).first()
        if code != request.session['v_code']:
            msg = '验证码不正确'
            return render(request, 'home/user/login.html', {'msg': msg})

        if user:
            # 验证密码是否正确

            if check_password(password, user.password):
                # 1. 保存ticket在客户端
                ticket = get_ticket()
                response = HttpResponseRedirect('/user/user_home/')
                out_time = datetime.now() + timedelta(days=30)
                response.set_cookie('ticket', ticket, expires=out_time)
                # 2. 保存ticket到服务端的user_ticket表中
                UserTicket.objects.create(user=user,
                                          out_time=out_time,
                                          ticket=ticket)

                return response
            else:
                msg = '密码错误'
                return render(request, 'home/user/login.html', {'msg': msg})
        else:
            msg = '用户不存在'
            return render(request, 'home/user/login.html', {'msg': msg})


def user_logout(request):
    if request.method == 'GET':
        # 注销，删除当前登录的用户的cookies中的ticket信息
        response = HttpResponseRedirect('/user/user_login/')
        response.delete_cookie('ticket')

        return response


def user_home(request):
    user = get_user(request)

    if request.method == 'GET':
        data = {'user': user}

        return render(request, 'home/user/user_home.html', data)
    if request.method == 'POST':

        if not user.email:
            user.email = request.POST.get('email')
            if User.objects.filter(email=user.email).first():
                msg = '该邮箱已注册'
                return render(request, 'home/user/user_home.html', {'msg': msg})
            if not re.match("^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$", str(user.email)):
                msg = '请输入有效邮箱号'
                return render(request, 'home/user/user_home.html', {'msg': msg})

        if not user.icon:
            user.icon = request.FILES.get('icon')

        if not user.tel:
            user.tel = request.POST.get('tel')
            if User.objects.filter(tel=user.tel).first():
                msg = '该手机已注册'
                return render(request, 'home/user/user_home.html', {'msg': msg})
            if not re.match("^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$", str(user.tel)):
                msg = '请输入有效手机号'
                return render(request, 'home/user/user_home.html', {'msg': msg})

        if user.sex is None:
            user.sex = 1 if request.POST.get('sex') == '男' else 0
        user.save()

        return HttpResponseRedirect('/user/user_home/')


def user_collection(request):
    user = get_user(request)
    focus = Focus.objects.filter(user=user)
    goods = []
    for f in focus:
        goods.append(f.goods)
    data = {'goods': goods}
    return render(request, 'home/user/collection.html', data)


def user_comment(request):
    user = get_user(request)
    comments = Comments.objects.filter(user=user)

    data = {'comments': comments}
    return render(request, 'home/user/comment.html', data)
