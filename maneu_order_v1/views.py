from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import reverse

from common import verify
from common import common
from common.excel import excel_save
from maneu_order_v1 import service
from maneu_order_v1.forms.BatchInsertForm import BatchInsertForm
import datetime


def index(request):
    if request.GET.get('time'):
        time = request.GET.get('time')
    else:
        time = common.today()
    date = datetime.datetime.strptime(time, '%Y-%m-%d')
    down_day = (date + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
    up_day = (date + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    list = service.batch_userid(userid=request.session.get('id'), time=time)  # 查找今日订单
    return render(request, 'maneu_order_v1/index.html', {'list': list,
                                                      'time': time,
                                                      'up_day': up_day,
                                                      'down_day': down_day})


def detail(request):
    if request.GET.get('id'):
        order = service.batch_detail(id=request.GET.get('id'))
        return render(request, 'maneu_order_v1/detail.html', {'order': order})
    else:
        return HttpResponseRedirect(reverse('maneu_order_v1:index'))


def delete(request):
    if request.GET.get('id'):
        service.batch_delete(id=request.GET.get('id'))
    return HttpResponseRedirect(reverse('maneu_order_v1:index'))


def insert(request):
    msg = None
    if request.method == 'POST':
        form = BatchInsertForm(request.POST)
        excel = request.FILES.get('excel')
        if form.is_valid() and excel:
            order = excel_save(excel, order_id)
            service.batch_insert(form.clean(), order, order_id)
            return index(request)
        msg = '参数错误'
    return render(request, 'maneu_order_v1/insert.html', {'msg': msg})


def search(request):
    """查找指定订单"""
    date = verify.date_method_post(request)
    if date:
        orderlist = service.find_batch_date(date=date)  # 查找今日订单
        return render(request, 'maneu_order_v1/index.html', {'orderlist': orderlist})
    return HttpResponseRedirect(reverse('maneu_order_v2:order_list'))