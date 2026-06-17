import datetime

from django.shortcuts import HttpResponseRedirect, reverse, render

from common import common
from maneu_alterSales import service


# Create your views here.


def index(request):
    if request.GET.get('time'):
        time = request.GET.get('time')
    else:
        time = common.today()
    date = datetime.datetime.strptime(time, '%Y-%m-%d')
    down_day = (date + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
    up_day = (date + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    list = service.ManeuService_index(time=time)  # 查找今日订单
    return render(request, 'maneu_afterSales/index.html',
                  {'list': list, 'time': time, 'up_day': up_day, 'down_day': down_day})


def list(request):
    order_id = request.session.get('order_id')
    if order_id:
        return render(request, 'maneu_afterSales/list.html',
                      {'alterSalesList': service.ManeuService_orderID(order_id=order_id)})
    return HttpResponseRedirect(reverse('maneu_order:index'))


def content(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        ManeuService_list = service.ManeuService_orderID(order_id)
        return render(request, 'maneu_afterSales/detail.html', {'alterSalesContent': ManeuService_list})
    else:
        return HttpResponseRedirect(reverse('maneu_order:index'))


def insert(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        content = request.POST.get('content')
        insert = service.ManeuService_insert(content=content, order_id=order_id)
        return HttpResponseRedirect(reverse('maneu_alterSales:alterSalesList'))
    elif request.method == 'GET':
        order_id = request.session.get('order_id')
        return render(request, 'maneu_afterSales/insert.html', {'order_id': order_id})
    else:
        return HttpResponseRedirect(reverse('index'))


def delete(request):
    if request.method == 'POST':
        insert = service.ManeuService_delete_id(id=request.POST.get('order_id'))
    return HttpResponseRedirect(reverse('maneu_alterSales:alterSalesList'))
