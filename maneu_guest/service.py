from django.db.models import Q

from maneu.models import *


def guest_search_text(admin_id='', value=''):
    return ManeuGuest.objects.filter(Q(name__icontains=value, admin_id=admin_id) | Q(phone__icontains=value, admin_id=admin_id)).order_by('-time').all()


def guest_search_time(admin_id='', timeS='', timeE=''):
    return ManeuGuest.objects.filter(admin_id=admin_id, time__gte=timeS, time__lte=timeE).order_by('-time').all()


def ManeuGuest_get(admin_id='', phone=''):
    return ManeuGuest.objects.filter(admin_id=admin_id, phone=phone).first()


def ManeuGuest_detail(admin_id='', id=''):
    return ManeuGuest.objects.filter(admin_id=admin_id, id=id).first()


def ManeuGuest_insert(admin_id='', time='', name='', phone='', sex='', age='', ot='', em='', dfh='', remark=''):
    return ManeuGuest.objects.create(admin_id=admin_id, name=name, phone=phone, time=time, sex=sex, age=age, ot=ot, em=em, dfh=dfh, remark=remark)


def ManeuGuest_update(admin_id='', id='', time='', name='', phone='', sex='', age='', ot='', em='', dfh='', remark=''):
    return ManeuGuest.objects.filter(id=id, admin_id=admin_id).update(time=time, name=name, phone=phone, sex=sex,
                                                                      age=age, ot=ot, em=em, dfh=dfh, remark=remark)


def ManeuGuest_delete(id='', admin_id=''):
    return ManeuGuest.objects.filter(id=id, admin_id=admin_id).delete()
