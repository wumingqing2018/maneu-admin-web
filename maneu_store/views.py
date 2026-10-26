from django.shortcuts import render

from common.util_time import time_now, time_start, time_end


def index(request):
    return render(request, 'store_index.html', {'timeS': time_start, 'timeE': time_end})


def insert(request):
    return render(request, 'store_insert.html')


def detail(request):
    return render(request, 'store_detail.html', {'index_id': request.GET.get('index_id')})
