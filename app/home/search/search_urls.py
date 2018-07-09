from django.urls import path

from app.home.search import search_api

urlpatterns = [
    # 商品搜索
    path(r'search/', search_api.search_goods, name='search_goods'),
    path(r'index/', search_api.index, name='index'),
]