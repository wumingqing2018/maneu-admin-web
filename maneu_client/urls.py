from django.urls import path

from maneu_client import views

app_name = 'maneu_client'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('insert/', views.insert, name='insert'),
    path('detail/', views.detail, name='detail'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('search/', views.search, name='search'),
    path('orderList/', views.order_list, name='orderList'),
    path('detailPhone/', views.detail_phone, name='detail_phone'),

]
