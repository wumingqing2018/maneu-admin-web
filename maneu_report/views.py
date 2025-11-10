from django.shortcuts import render

from common.common import current_time, time_start, time_end


def index(request):
    return render(request, 'maneu_report/index.html', {'timeS': time_start, 'timeE': time_end})


def insert(request):
    return render(request, 'maneu_report/insert.html', {'time': current_time()})


def detail(request):
    return render(request, 'maneu_report/detail.html', {'report_id': request.GET.get('id'), 'guest_id': request.GET.get('guest_id')})
