from django.db.models import Q

from maneu.models import *


def guest_insert(admin_id='', index_id='', time='', name='', phone='', status='', sex='', age='', ot='', em='', dfh='', remark=''):
    return ManeuGuest.objects.create(admin_id=admin_id, id=index_id, name=name, phone=phone, time=time, sex=sex, age=age, ot=ot, em=em, dfh=dfh, remark=remark, status=status)


def guest_delete(admin_id='', index_id=''):
    return ManeuGuest.objects.filter(admin_id=admin_id, id=index_id).first().delete()


def guest_detail(admin_id='', id=''):
    return ManeuGuest.objects.filter(admin_id=admin_id, id=id).first()


def guest_search_time(admin_id='', timeS='', timeE=''):
    return ManeuGuest.objects.filter(admin_id=admin_id, time__gte=timeS, time__lte=timeE).order_by('-time').all()


def guest_search_data(admin_id='', value=''):
    return ManeuGuest.objects.filter(Q(name__icontains=value, admin_id=admin_id) | Q(phone__icontains=value, admin_id=admin_id)).order_by('-time').all()


def guest_update_time(admin_id='', guest_id='', time=""):
    return ManeuGuest.objects.filter(id=guest_id, admin_id=admin_id).update(time=time)


def guest_update_data(admin_id='', guest_id='', time='', name='', phone='', sex='', age='', ot='', em='', dfh='', remark=''):
    return ManeuGuest.objects.filter(id=guest_id, admin_id=admin_id).update(name=name, time=time, phone=phone, sex=sex, age=age, ot=ot, em=em, dfh=dfh, remark=remark)
