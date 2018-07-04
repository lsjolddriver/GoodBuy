from django.urls import path

from app.admin.admin_user_manage import admin_user_manage_api

urlpatterns = [
    path('',admin_user_manage_api.admin_user_manage),
]