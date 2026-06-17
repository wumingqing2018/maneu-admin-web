from django.shortcuts import render

from common.common import current_time, time_start, time_end


def index(request):
    return render(request, 'report_index.html', {'timeS': time_start, 'timeE': time_end})


def insert(request):
    return render(request, 'report_insert.html', {'time': current_time()})


def detail(request):
    return render(request, 'report_detail.html', {'index_id': request.GET.get('index_id')})
