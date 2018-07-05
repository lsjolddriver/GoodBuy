from django.urls import path

from app.admin.admin_page import admin_page_api

urlpatterns = [
    path('login/', admin_page_api.login),
    path('index/', admin_page_api.admin_page),
    path('main/', admin_page_api.admin_main),
    path('top/', admin_page_api.admin_top),
    path('menu/', admin_page_api.admin_menu),
]