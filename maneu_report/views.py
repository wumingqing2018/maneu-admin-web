from uuid import uuid4

from django.shortcuts import render

from common.common import current_time, time_start, time_end


def index(request):
    return render(request, 'maneu_report/index.html', {'timeS': time_start, 'timeE': time_end, 'mark': uuid4()})


def insert(request):
    return render(request, 'maneu_report/insert.html', {'time': current_time(), 'mark': uuid4()})


def detail(request):
    return render(request, 'maneu_report/detail.html', {'id': request.GET.get('id'), 'mark': uuid4()})
