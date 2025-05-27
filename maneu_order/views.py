from django.shortcuts import render
from common.common import *

def index(request):
    return render(request, 'maneu_order/index.html', {'timeS': time_start, 'timeE': time_end})


def insert(request):
    return render(request, 'maneu_order/insert.html', {'time': current_time()})


def detail(request):

    token = get_miniprogram_token()

    print(get_wxacode(token, code=request.GET.get('id')))

    return render(request, 'maneu_order/detail.html', {'order_id': request.GET.get('id')})
