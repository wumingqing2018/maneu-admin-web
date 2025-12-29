from django.db.models import Q

from maneu.models import ManeuAdmin, ManeuGuest, ManeuReport
from maneu.models import ManeuOrder


def get_access_token(code=''):
    return ManeuAdmin.objects.filter(id=code).first()


def update_access_token(content):
    return ManeuAdmin.objects.all().update(content=content)


def guest_detail(admin_id='', guest_id=''):
    return ManeuGuest.objects.filter(id=guest_id, admin_id=admin_id).first()


def report_detail(admin_id='', report_id=''):
    return ManeuReport.objects.filter(id=report_id, admin_id=admin_id).first()


def order_detail(admin_id='', order_id=''):
    return ManeuOrder.objects.filter(id=order_id, admin_id=admin_id).first()


def guest_delete(admin_id='', guest_id=''):
    return ManeuGuest.objects.filter(admin_id=admin_id, id=guest_id).delete()


def order_delete(admin_id='', order_id=''):
    return ManeuOrder.objects.filter(admin_id=admin_id, id=order_id).delete()


def report_delete(admin_id='', report_id=''):
    return ManeuReport.objects.filter(admin_id=admin_id, id=report_id).delete()


def order_search_text(admin_id='', value=''):
    return ManeuOrder.objects.filter(Q(name__icontains=value, admin_id=admin_id) | Q(phone__icontains=value, admin_id=admin_id)).order_by('-time').all()


def order_search_time(admin_id='', timeS='', timeE=''):
    return ManeuOrder.objects.filter(admin_id=admin_id, time__gte=timeS, time__lte=timeE).order_by('-time').all()


def order_insert(admin_id='', name='', time='', phone='', status='', content='', guest_id='', store_id='', report_id='', remark=''):
    return ManeuOrder.objects.create(name=name, time=time, phone=phone, status=status, guest_id=guest_id, admin_id=admin_id, store_id=store_id, report_id=report_id, remark=remark, content=content)


def order_update(admin_id='', order_id='', name='', call='', time="", remark="", content=''):
    return ManeuOrder.objects.filter(id=order_id, admin_id=admin_id).update(name=name, phone=call, time=time, remark=remark, content=content)
