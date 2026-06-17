from django.urls import path

from maneu_alterSales import views

app_name = 'maneu_alterSales'
urlpatterns = [
    # views
    path('list/', views.list, name='list'),
    path('index/', views.index, name='index'),
    path('insert/', views.insert, name='alterSalesInsert'),
    path('delete/', views.delete, name='alterSalesDelete'),
    path('content/', views.content, name='alterSalesContent'),
]
