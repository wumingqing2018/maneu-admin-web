from django.urls import path

from maneu_index import api, views

app_name = 'maneu_index'
urlpatterns = [
    path('', views.index, name='index'),
    path('api_search_time/', api.search_time, name='api_search_time'),
    path('api_search_data/', api.search_data, name='api_search_data'),
]
