from django.shortcuts import render

from common.common import time_start, time_end


def index(request):
    return render(request, 'maneu_index/index.html', {'timeS': time_start, 'timeE': time_end})


def detail(request):
    return render(request, 'maneu_admin/index.html', {'id': request.session.get('id')})


def insert(request):
    return render(request, 'maneu_admin/insert.html', {'id': request.session.get('id')})


def update(request):
    return render(request, 'maneu_admin/insert.html', {'id': request.session.get('id')})
