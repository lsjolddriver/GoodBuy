from django.urls import path

from app.home.user import user_api

urlpatterns = [
    path('', user_api.register),
    path('', user_api.login),
    path('', user_api.logout),
]