from django.shortcuts import render

from common import common
from maneu.models import ManeuStore, ManeuOrder
import json


def index(request):
    return render(request, 'maneu_store/index.html', {'timeS': common.time_start, 'timeE': common.time_end})


def insert(request):
    return render(request, 'maneu_store/insert.html', {'time': common.current_time()})


def detail(request):
    return render(request, 'maneu_store/detail.html',{'index_id': request.GET.get('index_id')})
