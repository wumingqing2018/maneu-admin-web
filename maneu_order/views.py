from django.shortcuts import render

from common import common


def index(request):
    return render(request, 'maneu_order/index.html', {'timeS': common.time_start, 'timeE': common.time_end})


def insert(request):
    return render(request, 'maneu_order/insert.html', {'time': common.current_time()})


def detail(request):
    return render(request, 'maneu_order/detail.html',{'index_id': request.GET.get('index_id')})
