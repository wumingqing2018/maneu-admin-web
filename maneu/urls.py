from django.urls import include
from django.urls import path

from maneu.api import *
from maneu.views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('sendsms/', sendsms, name='sendsms'),
    path('access_token/', access_token, name='access_token'),
    path('remove_token/', remove_token, name='remove_token'),
    path('refresh_token/', refresh_token, name='refresh_token'),
    path('maneu_admin/', include('maneu_admin.urls')),
    path('maneu_guest/', include('maneu_guest.urls')),
    path('maneu_index/', include('maneu_index.urls')),
    path('maneu_order/', include('maneu_order.urls')),
    path('maneu_store/', include('maneu_store.urls')),
    path('maneu_report/', include('maneu_report.urls')),
    path('maneu_repair/', include('maneu_repair.urls')),
]
