from django.urls import path

from maneu_datalogs import views

app_name = 'maneu_datalogs'
urlpatterns = [
    # views
    path('index/', views.index, name='index'),
]
