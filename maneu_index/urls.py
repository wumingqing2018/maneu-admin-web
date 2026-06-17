from django.urls import path

from maneu_index import api, views

app_name = 'maneu_index'
urlpatterns = [
    path('', views.index, name='index'),
    path('api_statistics/', api.statistics, name='api_statistics'),
]
