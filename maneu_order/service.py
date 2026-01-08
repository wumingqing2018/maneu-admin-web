from django.db.models import Q

from maneu.models import ManeuOrder


def order_insert(admin_id='', name='', time='', phone='', status='', content='', guest_id='', store_id='', report_id='', remark=''):
    return ManeuOrder.objects.create(name=name, time=time, phone=phone, status=status, guest_id=guest_id, admin_id=admin_id, store_id=store_id, report_id=report_id, remark=remark, content=content)


def order_delete(admin_id='', order_id=''):
    return ManeuOrder.objects.filter(admin_id=admin_id, id=order_id).delete()


def order_detail(admin_id='', order_id=''):
    return ManeuOrder.objects.filter(id=order_id, admin_id=admin_id).first()


def order_search_time(admin_id='', timeS='', timeE=''):
    return ManeuOrder.objects.filter(admin_id=admin_id, time__gte=timeS, time__lte=timeE).order_by('-time').all()


def order_search_data(admin_id='', value=''):
    return ManeuOrder.objects.filter(Q(name__icontains=value, admin_id=admin_id) | Q(phone__icontains=value, admin_id=admin_id)).order_by('-time').all()


def order_update_time(admin_id='', order_id='', time=""):
    return ManeuOrder.objects.filter(id=order_id, admin_id=admin_id).update(time=time)


def order_update_data(admin_id='', order_id='', name='', call='', remark="", content=''):
    return ManeuOrder.objects.filter(id=order_id, admin_id=admin_id).update(name=name, phone=call, remark=remark, content=content)
