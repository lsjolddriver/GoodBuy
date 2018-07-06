"""
装饰器类,访问页面,登录验证,接口访问登录验证
AUTH: Jason
DATE: 2018年7月5日 09:49:38
"""

from functools import wraps
from django.http.response import HttpResponseRedirect


def is_login(fn):
    """
    访问页面时的登录的验证
    未登录会跳转到登录页面
    :param fn:  需要判断的方法
    :return: 返回具体页面
    """

    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        try:
            user_id = request.session['admin_user_id']
            print(user_id)
        except KeyError as e:
            print('有用户未登录', str(e))
            return HttpResponseRedirect('/admin_page/login/')
        else:
            return fn(request, *args, **kwargs)

    return wrapper