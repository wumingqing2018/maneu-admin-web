from django.urls import path

from maneu_guest import views, api

app_name = 'maneu_guest'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/', views.detail, name='detail'),
    path('insert/', views.insert, name='insert'),
    path('api_insert/', api.insert, name='api_insert'),
    path('api_detail/', api.detail, name='api_detail'),
    path('api_delete/', api.delete, name='api_delete'),
    path('search_time/', api.search_time, name='search_time'),
    path('search_data/', api.search_data, name='search_text'),
    path('update_time/', api.update_time, name='update_time'),
    path('update_data/', api.update_data, name='update_data'),
]
