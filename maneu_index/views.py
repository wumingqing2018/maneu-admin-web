from django.shortcuts import render

from common.common import time_start, time_end


def index(request):
    return render(request, 'maneu_index/index.html', {'timeS': time_start, 'timeE': time_end})
