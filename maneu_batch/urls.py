from django.urls import path

from maneu_batch import views

app_name = 'maneu_batch'
urlpatterns = [
    # views
    path('index/', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('insert/', views.insert, name='insert'),
    path('delete/', views.delete, name='delete'),
    path('detail/', views.detail, name='detail'),
]
