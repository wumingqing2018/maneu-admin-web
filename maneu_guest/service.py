from django.db.models import Q

from maneu.models import *


def ManeuGuest_index(admin_id='', start='', end=''):
    return ManeuGuest.objects.filter(admin_id=admin_id, time__gte=start, time__lte=end).order_by('-time').all()


def guest_search(admin_id, timeS, timeE, value):
    return ManeuGuest.objects.filter(
        Q(name__icontains=value, admin_id=admin_id, time__gte=timeS, time__lte=timeE, ) | Q(phone__icontains=value,
                                                                                            admin_id=admin_id,
                                                                                            time__gte=timeS,
                                                                                            time__lte=timeE, )).order_by(
        '-time').all()


def ManeuGuest_detail(admin_id='', id=''):
    return ManeuGuest.objects.filter(admin_id=admin_id, id=id).first()


def ManeuGuest_insert(admin_id='', time='', name='', phone='', sex='', age='', ot='', em='', dfh='', remark=''):
    return ManeuGuest.objects.get_or_create(admin_id=admin_id, name=name, phone=phone,
                                            defaults={'sex': sex, 'age': age, 'ot': ot, 'em': em, 'dfh': dfh,
                                                      'time': time, 'remark': remark})


def ManeuGuest_update(admin_id='', id='', time='', name='', phone='', sex='', age='', ot='', em='', dfh='', remark=''):
    return ManeuGuest.objects.filter(id=id, admin_id=admin_id).update(time=time, name=name, phone=phone, sex=sex,
                                                                      age=age, ot=ot, em=em, dfh=dfh, remark=remark)


def ManeuGuest_delete(id='', admin_id=''):
    return ManeuGuest.objects.filter(id=id, admin_id=admin_id).delete()
