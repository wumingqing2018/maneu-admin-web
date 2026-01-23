from django.urls import path

from maneu_index import api, views

app_name = 'maneu_index'
urlpatterns = [
    path('', views.index, name='index'),
    path('search_time/', api.search_time, name='search_time'),
    path('search_data/', api.search_data, name='search_text'),

]
