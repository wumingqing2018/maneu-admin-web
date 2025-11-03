from uuid import uuid4

from django.shortcuts import render

from common import common


def index(request):
    print(common.time_start, common.time_end)
    return render(request, 'maneu_order/index.html', {'timeS': common.time_start, 'timeE': common.time_end, 'mark': str(uuid4())})


def insert(request):
    return render(request, 'maneu_order/insert.html', {'time': common.current_time(), 'mark': str(uuid4())})


def detail(request):
    return render(request, 'maneu_order/detail.html', {'order_id': request.GET.get('id'), 'mark': str(uuid4())})
