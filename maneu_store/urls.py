from django.urls import path

from maneu_store import api
from maneu_store import views

app_name = 'maneu_store'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/', views.detail, name='detail'),
    path('insert/', views.insert, name='insert'),
    path('api_detail/', api.detail, name='api_detail'),
    path('api_insert/', api.insert, name='api_insert'),
    path('api_delete/', api.delete, name='api_delete'),
    path('api_QRcode/', api.qrcode, name='api_QRcode'),
    path('api_update_time/', api.update_time, name='api_update_time'),
    path('api_update_data/', api.update_data, name='api_update_data'),
    path('api_search_time/', api.search_time, name='api_search_time'),
    path('api_search_data/', api.search_data, name='api_search_data'),
]
