from django.shortcuts import render

from maneu.models import *


def index(request):
    ManeuGuest.objects.filter().all().update(status='')


    orderList = ManeuOrder.objects.all()
    for order in orderList:
        guest = ManeuGuest.objects.filter(id=order.guest_id).first()
        if guest is None:
            guest = ManeuGuest.objects.create(id=order.id, admin_id=order.admin_id, time=order.time, name=order.name, phone=order.phone, status=3, remark=order.remark)
        else:
            guest.id = order.id
            guest.save()

        report = ManeuReport.objects.filter(id=order.report_id).first()
        if report is None:
            report = ManeuReport.objects.create(id=order.id, admin_id=order.admin_id, time=order.time, name=order.name, phone=order.phone, status=3, remark=order.remark, od_va=0.00, os_va=0.00, os_sph=0.00, od_sph=0.00, od_cyl=0.00, os_cyl=0.00, od_add=0.00, os_add=0.00)
        else:
            report.id = order.id
            report.save()
        print(report.id)


    reportList = ManeuReport.objects.exclude(status=3).all()
    for report in reportList:
        guest = ManeuGuest.objects.filter(id=report.guest_id).first()
        if guest is None:
            guest = ManeuGuest.objects.create(id=report.id, admin_id=report.admin_id, time=report.time, name=report.name, phone=report.phone, status=2, remark=report.remark)
        else:
            guest.id = report.id
            guest.save()


    ManeuGuest.objects.filter(status='').all().delete()

    return render(request, 'maneu/index.html')


def login(request):
    return render(request, 'maneu/login.html')
