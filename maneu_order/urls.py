from django.urls import path

from maneu_order import views

app_name = 'maneu_order'
urlpatterns = [
    # views
    path('index/', views.index, name='index'),
    path('delete/', views.delete, name='delete'),
    path('detail/', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    path('insert/', views.insert, name='insert'),
    path('update/', views.update, name='update'),

    # api
    # path('api_order_list/', api.order_list, name='api_order_list'),
    # path('api_order_qrcode/', api.order_qrcode, name='api_order_qrcode'),
    # path('api_order_detail/', api.order_detail, name='api_order_detail'),
    # path('api_order_insert/', api.order_insert, name='api_order_insert'),
    # path('api_order_update/', api.order_update, name='api_order_update'),
    # path('api_order_delete/', api.order_delete, name='api_order_delete'),
]
