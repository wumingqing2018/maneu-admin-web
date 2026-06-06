from django.urls import path

from maneu_report import api, views

app_name = 'maneu_report'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/', views.detail, name='detail'),
    path('insert/', views.insert, name='insert'),
    path('api_insert/', api.insert, name='api_insert'),
    path('api_detail/', api.detail, name='api_detail'),
    path('api_delete/', api.delete, name='api_delete'),
    path('api_update/', api.update, name='api_update'),
    path('api_QRcode/', api.generate_qr_code, name='api_QRcode'),
    path('api_search_time/', api.search_time, name='api_search_time'),
    path('api_search_data/', api.search_data, name='api_search_data'),
]
