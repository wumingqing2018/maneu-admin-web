from django.shortcuts import render

from maneu.models import *


def index(request):
    orderList = ManeuOrder.objects.all()
    for order in orderList:
        guest = ManeuGuest.objects.filter(id=order.guest_id).first()
        guest = ManeuGuest.objects.create(admin_id=guest.admin_id, time=guest.time, name=guest.name, phone=guest.phone, status=3, sex=guest.sex, age=guest.age, dfh=guest.dfh, ot=guest.ot, em=guest.em, remark=guest.remark)
        print(ManeuReport.objects.filter(id=order.report_id).update(status=3, guest_id=guest.id))

    reportList = ManeuReport.objects.exclude(status=3).all()
    for report in reportList:
        try:
            guest = ManeuGuest.objects.filter(id=report.guest_id).first()
            guest = ManeuGuest.objects.create(admin_id=guest.admin_id, time=guest.time, name=guest.name,
                                              phone=guest.phone, status=3, sex=guest.sex, age=guest.age, dfh=guest.dfh,
                                              ot=guest.ot, em=guest.em, remark=guest.remark)
            ManeuReport.objects.filter(id=report.id).update(status=2, guest_id=guest.id)
        except:
            print(report.id)



    return render(request, 'maneu/index.html')


def login(request):
    return render(request, 'maneu/login.html')
