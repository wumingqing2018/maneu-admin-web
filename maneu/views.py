from django.shortcuts import render
from maneu.models import *


def index(request):

    orderList = ManeuOrder.objects.all()
    for order in orderList:
        print(ManeuReport.objects.filter(id=order.report_id).update(status=3))
    print(ManeuReport.objects.filter(status__isnull=True).update(status=2))

    return render(request, 'maneu/index.html')


def login(request):
    return render(request, 'maneu/login.html')
