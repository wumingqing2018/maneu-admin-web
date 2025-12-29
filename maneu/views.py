from django.shortcuts import render

from maneu.models import *


def index(request):
    ManeuGuest.objects.filter().all().update(status='')

    orderList = ManeuOrder.objects.all()
    for order in orderList:
        guest = ManeuGuest.objects.filter(id=order.guest_id).first()
        guest2 = ManeuGuest.objects.create(admin_id=order.admin_id, time=order.time, name=order.name, phone=order.phone, status=3, sex=guest.sex, age=guest.age, dfh=guest.dfh, ot=guest.ot, em=guest.em, remark=guest.remark)
        print(ManeuReport.objects.filter(id=order.report_id).update(status=3, guest_id=guest2.id))
        order.guest_id = guest2.id
        order.save()

    reportList = ManeuReport.objects.exclude(status=3).all()
    for report in reportList:
        guest = ManeuGuest.objects.filter(id=report.guest_id).first()
        try:
            guest2 = ManeuGuest.objects.create(admin_id=report.admin_id, time=report.time, name=report.name,
                                              phone=report.phone, status=2, sex=guest.sex, age=guest.age, dfh=guest.dfh,
                                              ot=guest.ot, em=guest.em, remark=guest.remark)
        except:
            guest2 = ManeuGuest.objects.create(admin_id=report.admin_id, time=report.time, name=report.name, phone=report.phone, status=2, remark=report.remark)
            print(guest2)
        ManeuReport.objects.filter(id=report.id).update(status=2, guest_id=guest2.id)

    ManeuGuest.objects.filter(status='').all().delete()

    return render(request, 'maneu/index.html')


def login(request):
    return render(request, 'maneu/login.html')
