from django.db.models import Q

from maneu.models import ManeuOrder


def order_insert(admin_id='', index_id='', name='', time='', phone='', status='', content='', guest_id='', store_id='', report_id='', remark=''):
    return ManeuOrder.objects.create(id=index_id, name=name, time=time, phone=phone, status=status, guest_id=guest_id, admin_id=admin_id, store_id=store_id, report_id=report_id, remark=remark, content=content)


def order_delete(admin_id='', index_id=''):
    return ManeuOrder.objects.filter(admin_id=admin_id, id=index_id).delete()


def order_detail(admin_id='', index_id=''):
    return ManeuOrder.objects.filter(admin_id=admin_id, id=index_id).first()


def order_search_time(admin_id='', timeS='', timeE=''):
    return ManeuOrder.objects.filter(admin_id=admin_id, time__gte=timeS, time__lte=timeE).order_by('-time').all()


def order_search_data(admin_id='', value=''):
    return ManeuOrder.objects.filter(Q(name__icontains=value, admin_id=admin_id) | Q(phone__icontains=value, admin_id=admin_id)).order_by('-time').all()


def order_update_time(admin_id='', index_id='', time="", name="", phone=""):
    return ManeuOrder.objects.filter(admin_id=admin_id, id=index_id).update(time=time, name=name, phone=phone)


def order_update_data(admin_id='', index_id='', remark="", content=''):
    return ManeuOrder.objects.filter(admin_id=admin_id, id=index_id).update(remark=remark, content=content)

