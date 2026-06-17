from django.urls import include
from django.urls import path

from maneu.views import *

urlpatterns = [
    # 首页
    path('', index, name='index'),
    # 登录页
    path('login/', login, name='login'),
    # 订单子路由
    path('maneu_order/', include('maneu_order.urls')),
    # 用户子路由
    path('maneu_users/', include('maneu_users.urls')),
    # 用户子路由
    path('maneu_client/', include('maneu_client.urls')),
    # 批发子路由
    path('maneu_batch/', include('maneu_batch.urls')),
    # 商品子路由
    path('maneu_class/', include('maneu_class.urls')),
    # 商品子路由
    path('maneu_datalogs/', include('maneu_datalogs.urls')),
    path('maneu_alterSales/', include('maneu_alterSales.urls')),
]
