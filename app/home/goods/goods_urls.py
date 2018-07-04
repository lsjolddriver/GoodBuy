from django.urls import path

from app.home.goods import goods_api

urlpatterns = [
    path('', goods_api.goods),
]