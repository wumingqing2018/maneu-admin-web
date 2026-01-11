from django.urls import path

from maneu_order import api
from maneu_order import views

app_name = 'maneu_order'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/', views.detail, name='detail'),
    path('insert/', views.insert, name='insert'),
    path('api_detail/', api.detail, name='api_detail'),
    path('api_insert/', api.insert, name='api_insert'),
    path('api_delete/', api.delete, name='api_delete'),
    path('api_update/', api.update, name='api_update'),
    path('search_time/', api.search_time, name='search_time'),
    path('search_data/', api.search_data, name='search_data'),
]
