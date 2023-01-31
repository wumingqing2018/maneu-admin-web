from django.shortcuts import HttpResponseRedirect, reverse
from django.shortcuts import render

from maneu_alterSales import service


# Create your views here.
def list(request):
    order_id = request.session.get('order_id')
    if order_id:
        return render(request, 'maneu_afterSales/list.html', {'alterSalesList': service.ManeuAfterSales_list(order_id=order_id)})
    return HttpResponseRedirect(reverse('maneu_order:order_list'))


def index(request):
    return render(request, 'maneu_afterSales/index.html', {'alterSalesList': service.ManeuAfterSales_index()})


def content(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        ManeuAfterSales_list = service.ManeuAfterSales_list(order_id)
        return render(request, 'maneu_afterSales/detail.html', {'alterSalesContent': ManeuAfterSales_list})
    else:
        return HttpResponseRedirect(reverse('maneu_order:order_list'))


def insert(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        content = request.POST.get('content')
        insert = service.ManeuAfterSales_insert(content=content, order_id=order_id)
        return HttpResponseRedirect(reverse('maneu_alterSales:alterSalesList'))
    elif request.method == 'GET':
        order_id = request.session.get('order_id')
        return render(request, 'maneu_afterSales/insert.html', {'order_id': order_id})
    else:
        return HttpResponseRedirect(reverse('index'))


def delete(request):
    if request.method == 'POST':
        insert = service.ManeuAfterSales_delete_id(id=request.POST.get('order_id'))
    return HttpResponseRedirect(reverse('maneu_alterSales:alterSalesList'))


def error(request, message=''):
    return render(request, 'maneu_afterSales/error.html', {'message': message})
