from django.shortcuts import render

from common import common
from maneu_order import service


def index(request):
    return render(request, 'maneu_order/index.html', {'timeS': common.time_start, 'timeE': common.time_end})


def insert(request):
    return render(request, 'maneu_order/insert.html', {'time': common.current_time()})


def detail(request):
    data_token = service.get_access_token(code=request.session['id']).content
    get_wxacode = common.get_wxacode(access_token=data_token, code=request.GET.get('id'))
    if get_wxacode['code'] != 200:
        data_token = common.get_miniprogram_token()['access_token']
        print(1, service.update_access_token(content=data_token))
        print(2, common.get_wxacode(access_token=data_token, code=request.GET.get('id')))
    else:
        print(get_wxacode)

    return render(request, 'maneu_order/detail.html', {'order_id': request.GET.get('id')})
