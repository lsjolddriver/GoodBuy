"""
后台商品管理页面
AUTH:
DATE:
"""
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from app.models import Goods, Brand, Classification, SubclassificationBrand


def goods_list(request):
    # 商品列表
    if request.method == 'GET':

        goodslist = Goods.objects.all()
        brandlist = Brand.objects.all()
        classification = Classification.objects.all()

        data = {
            'goodslist': goodslist,
            'brandlist': brandlist,
            'classification': classification,
        }


        return render(request, 'admin/goodsList.html', data)


def goods_add(request):
    # 添加商品
    if request.method == 'POST':
        name = request.POST.get('name')
        c_price = request.POST.get('c_price')
        image = request.POST.get('image')
        description = request.POST.get('description')
        comments_amount = request.POST.get('comments_amount')
        sales_number = request.POST.get('goods_number')
        source = request.POST.get('source')
        subclassification_id = request.POST.get('cat_id')
        brand_id = request.POST.get('brand_id')

        Goods.objects.create(
            name=name,
            c_price=c_price,
            image=image,
            description=description,
            comments_amount=comments_amount,
            sales_number=sales_number,
            source=source,
            subclassification_id=subclassification_id,
            brand_id=brand_id
        )

    brand_lists = Brand.objects.all()
    classification_list = Classification.objects.all()

    data = {
        'brand_list': brand_lists,
        'classification_list': classification_list
    }

    return render(request, 'admin/goodsAdd.html', data)


def category_list(request):
    # 分类列表
    category_lists = Classification.objects.all()

    data = {
        'category_list': category_lists
    }
    return render(request, 'admin/categoryList.html', data)


def category_add(request):
    # 添加分类
    if request.method == 'POST':

        category_lists = request.POST.get('cat_name').split(',')

        for category in category_lists:

            Classification.objects.create(
                name=category
            )

    return render(request, 'admin/categoryAdd.html')


def category_change(request):
    # 改变分类名称
    myName = request.POST.get('myName')
    content = request.POST.get('content')
    category = Classification.objects.filter(name=myName).first()
    category.name = content # 改变数据
    category.save() # 存储

    data = {
        'code': 200,
        'msg': '改变成功'
    }

    return JsonResponse(data)


def category_remove(request):
    # 删除该分类
    myName = request.POST.get('myName')

    category = Classification.objects.filter(name=myName).first()

    category.delete()

    data = {
        'code': 200,
        'msg': '删除成功'
    }

    return JsonResponse(data)

def brand_list(request):
    # 品牌列表
    brand_lists = Brand.objects.all()
    data = {
        'brand_list': brand_lists
    }
    return render(request, 'admin/brandList.html', data)



def brand_add(request):
    # 添加品牌
    if request.method == 'POST':

        brand_lists = request.POST.get('brand_name').split(',')

        for brand in brand_lists:

            Classification.objects.create(
                name=brand
            )

    return render(request, 'admin/brandAdd.html')


def brand_change(request):
    # 改变品牌名称
    myName = request.POST.get('myName')
    content = request.POST.get('content')
    brand = Brand.objects.filter(name=myName).first()
    brand.name = content # 改变数据
    brand.save() # 存储

    data = {
        'code': 200,
        'msg': '改变成功'
    }

    return JsonResponse(data)


def brand_remove(request):

    # 删除该品牌
    myName = request.POST.get('myName')

    brand = Brand.objects.filter(name=myName).first()

    brand.delete()

    data = {
        'code': 200,
        'msg': '删除成功'
    }

    return JsonResponse(data)

