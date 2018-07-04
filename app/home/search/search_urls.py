from django.urls import path

from app.home.search import search_api

urlpatterns = [
    path('', search_api.search)
]