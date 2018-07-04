from django.urls import path

from app.admin.goods_manage import goods_manage_api

urlpatterns = [
    path('',goods_manage_api.goods_manage),
]