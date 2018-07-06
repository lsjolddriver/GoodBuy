"""
管理员账户管理页面
AUTH:
DATE:
"""
import jsonify as jsonify
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from app.models import AdminUser
import base64

# def admin_user_manage(request):
#     return render(request, 'Hello world')

def user_list(request):
    # 管理员列表
    if request.method == 'GET':
        super_name = AdminUser.objects.all()
        data = {
            'super_name': super_name
        }

    return render(request, 'admin/userList.html', data)

def look_user(request):
    # 查看管理员账号密码
    data = request.POST
    myName = data.get('myName')

    if myName:

        look = AdminUser.objects.filter(username=myName).first()
        password = look.password

        data = {
            'code': 200,
            'username': myName,
            'password': password
        }
        return JsonResponse(data)

    data = {
        'code': 200,
        'password': '没东西给你,滚!'
    }

    return JsonResponse(data)


def delete_user(request):
    # 删除该管理员账号
    myName = request.POST.get('myName')
    look = AdminUser.objects.filter(username=myName).first()
    look.delete()
    data = {
        'code': 200,
        'msg': '删除成功!'
    }
    return JsonResponse(data)




def user_add_page(request):
    # 添加管理员页面
    return render(request, 'admin/userAddPage.html')

def user_add(request):
    # 添加管理员按钮
    if request.method == 'GET':
        return render(request, 'admin/userAddPage.html')


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not all([username, password]):
            msg = '参数不能为空'
            return render(request, 'admin/userAddPage.html', {'msg': msg})
        password = make_password(password) # 密文存储
        AdminUser.objects.create(username=username,
                                 password=password,
                                 )
        return render(request, 'admin/userAddPage.html', {'msg': '添加成功'})



