"""
搜索页面
AUTH:
DATE:
"""
import re

import jieba
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http.response import HttpResponse

from app.models import Goods, Classification, Subclassification


def index(request):
    if request.method == 'GET':
        return render(request, '../templates/home/index.html')


def search_goods(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        source = request.GET.get('source')
        sort = request.GET.get('sort', 0)
        page_id = request.GET.get('page_id', 1)
        if key:
            # 过滤关键字的特殊符号
            filter_key = re.sub('[^\u4e00-\u9fa5_a-zA-Z0-9]', '', key)
            # 使用jieba分词将关键字进行分词
            # all_key = jieba.cut_for_search(filter_key)
            subclass = Subclassification.objects.filter(name=filter_key).first()
            sub_brands = subclass.subclassificationbrand_set.all() if subclass else None
            sub_classes = None
            if subclass:
                goods = subclass.goods_set.all()
            else:
                firclass = Classification.objects.filter(name__icontains=filter_key).first()
                class_list = firclass.subclassification_set.all() if firclass else None
                if class_list:
                    # 能搜索到一级分类
                    firclass_list = []
                    for cla in class_list:
                        firclass_list.append(cla.id)
                    goods = Goods.objects.filter(subclassification_id__in=firclass_list)
                    # 一级分类下的二级分类
                    sub_classes = Subclassification.objects.filter(id__in=class_list)
                else:
                    goods = Goods.objects.filter(name__icontains=filter_key)
            if sort == '0':
                # 默认排序
                goods = goods.order_by('id')
            elif sort == '1':
                # 价格升序
                goods = goods.order_by('c_price')
            elif sort == '2':
                # 价格降序
                goods = goods.order_by('-c_price')
            elif sort == '3':
                # 全网评论数排序
                goods = goods.order_by('-comments_amount')
            # 把商品进行分页处理, 每页2条数据
            page_count = 2
            paginator = Paginator(goods, page_count)
            page = paginator.page(int(page_id))
            return render(request, '../templates/home/list.html', {'goods': page,
                                                                   'key': filter_key,
                                                                   'sort': sort,
                                                                   'page_id': page_id,
                                                                   'sub_brands': sub_brands,
                                                                   'sub_classes': sub_classes,
                                                                   'page_count': page_count})
        return render(request, '../templates/home/list.html')

