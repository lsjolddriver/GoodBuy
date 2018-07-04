from django.urls import path

from app.admin.admin_page import admin_page_api

urlpatterns = [
    path('',admin_page_api.hello_admin_page),
]