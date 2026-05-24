from django.db.models import Q

from maneu.models import *


def guest_insert(admin_id='', index_id='', time='', name='', phone='', status='', content='', remark=''):
    return ManeuGuest.objects.create(admin_id=admin_id, id=index_id, name=name, phone=phone, time=time,
                                     sex=content['sex'], age=content['age'], ot=content['ot'], em=content['em'],
                                     dfh=content['dfh'], remark=remark, status=status)


def guest_delete(admin_id='', index_id=''):
    return ManeuGuest.objects.filter(admin_id=admin_id, id=index_id).first().delete()


def guest_detail(admin_id='', index_id=''):
    return ManeuGuest.objects.filter(admin_id=admin_id, id=index_id).first()


def guest_search_time(admin_id='', timeS='', timeE=''):
    return ManeuGuest.objects.filter(admin_id=admin_id, time__gte=timeS, time__lte=timeE).order_by('-time').all()


def guest_search_data(admin_id='', value=''):
    return ManeuGuest.objects.filter(
        Q(name__icontains=value, admin_id=admin_id) | Q(phone__icontains=value, admin_id=admin_id)).order_by(
        '-time').all()


def guest_update(admin_id='', index_id='', time='', name='', phone='', remark='', sex='', age="", ot='', em='', dfh=''):
    return ManeuGuest.objects.filter(admin_id=admin_id, id=index_id).update(name=name, phone=phone, time=time, sex=sex,
                                                                            age=age, ot=ot, em=em, dfh=dfh,
                                                                            remark=remark)


def order_update(admin_id='', index_id='', time="", name="", phone="", remark=''):
    return ManeuOrder.objects.filter(admin_id=admin_id, id=index_id).update(time=time, name=name, phone=phone,
                                                                            remark=remark)


def store_update(admin_id='', index_id='', time="", name="", phone="", remark=''):
    return ManeuStore.objects.filter(admin_id=admin_id, id=index_id).update(time=time, name=name, phone=phone,
                                                                            remark=remark)


def report_update(admin_id='', index_id='', time="", name="", phone="", remark=''):
    return ManeuReport.objects.filter(admin_id=admin_id, id=index_id).update(time=time, name=name, phone=phone,
                                                                             remark=remark)
