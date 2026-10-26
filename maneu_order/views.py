from django.shortcuts import render

from common.util_time import time_now, time_start, time_end


def index(request):
    return render(request, 'order_index.html')


def insert(request):
    return render(request, 'order_insert.html')


def detail(request):
    return render(request, 'order_detail.html')
