import redis
from django.utils.deprecation import MiddlewareMixin

from GoodBuy.settings import SESSION_REDIS


class AccessAmountMiddleware(MiddlewareMixin):
    """
    访问量中间件
    """
    conn = redis.Redis(host=SESSION_REDIS['host'], port=SESSION_REDIS['port'], password=SESSION_REDIS['password'])

    # 增加访问量并保存redis
    def SaveToRedis(self, name):
        num = int(self.conn.hget('access', name).decode('utf-8')) + 1 if self.conn.hexists('access', name) else 1
        self.conn.hset('access', name, num)

    # 访问量中间件
    def process_request(self, request):
        if request.path == '/home_page/index/':
            self.SaveToRedis('首页')
        if request.path == '/search/':
            self.SaveToRedis('搜索页面')
        if request.path == '/goods/':
            self.SaveToRedis('商品页面')
        if request.path == '/user/':
            self.SaveToRedis('个人中心页面')
        if request.path == '/home_page/login/':
            self.SaveToRedis('登录页面')
        if request.path == '/home_page/register/':
            self.SaveToRedis('注册页面')