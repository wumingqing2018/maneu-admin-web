from django.urls import path

from maneu_admin import views, api

app_name = 'maneu_admin'
urlpatterns = [
    path('', views.index, name='index'),
    path('insert/', views.insert, name='insert'),
    path('update/', views.update, name='update'),
    path('api_index/', api.index, name='api_index'),
    path('update_data/', api.update, name='api_update'),
]
