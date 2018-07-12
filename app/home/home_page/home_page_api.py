"""
前台首页
AUTH:
DATE:
"""
from django.shortcuts import render
from django.http.response import HttpResponse

# 首页
from app.models import Classification, Subclassification, Goods, Hot


def index_page(request):
    if request.method == 'GET':
        # 大类分类
        classification = Classification.objects.all()
        # 小类分类
        subclassification = Subclassification.objects.all()
        # 商品
        goods = Goods.objects.all()
        # 热门搜索
        hots = Hot.objects.all()

        data = {
            'classification': classification,
            'subclassification': subclassification,
            'goods': goods
        }
        return render(request, 'home/index.html', data)


# 分类查询
def list_page(request, cid):
    if request.method == 'GET':
        # 小类分类
        subclassification = Subclassification.objects.get(id=cid)
        # 大类分类
        classification = Classification.objects.filter(id=subclassification.classification_id)
        # 商品筛选
        goods = Goods.objects.filter(subclassification_id=cid)

        data = {
            'classification': classification,
            'subclassification': subclassification,
            'goods': goods
        }
        return render(request, 'home/list.html', data)
