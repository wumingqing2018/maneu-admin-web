from django.urls import include
from django.urls import path

from maneu.views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('sendsms/', sendsms, name='sendsms'),
    path('login_api/', login_api, name='login_api'),
    path('maneu_admin/', include('maneu_admin.urls')),
    path('maneu_guest/', include('maneu_guest.urls')),
    path('maneu_index/', include('maneu_index.urls')),
    path('maneu_order/', include('maneu_order.urls')),
    path('maneu_report/', include('maneu_report.urls')),
]
