"""GoodBuy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from app import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('verify_code/', views.verify_code),
    path('home_page/',include('app.home.home_page.home_page_urls')),
    path('search/',include('app.home.search.search_urls')),
    path('user/', include('app.home.user.user_urls')),
    path('', include('app.home.goods.goods_urls')),
    path('admin_page/', include('app.admin.admin_page.admin_page_urls')),
    path('admin_user_manage/', include('app.admin.admin_user_manage.admin_user_manage_urls')),
    path('goods_manage/', include('app.admin.goods_manage.goods_manage_urls')),
]
