from django.db.models import Q

from maneu.models import ManeuBuffer


def report_index(admin_id='', start='', end=''):
    return ManeuBuffer.objects.filter(admin_id=admin_id, time__gte=start, time__lte=end).order_by('-time').all()


def report_search(admin_id, timeS, timeE, value):
    return ManeuBuffer.objects.filter(Q(name__icontains=value, admin_id=admin_id, time__gte=timeS, time__lte=timeE, ) | Q(call__icontains=value, admin_id=admin_id, time__gte=timeS, time__lte=timeE, )).order_by('-time').all()


def report_delete(admin_id='', id=''):
    return ManeuBuffer.objects.filter(admin_id=admin_id, id=id).all().delete()


def report_insert(admin_id='', guest_id='', name='', time='', call='', remark='', content=''):
    return ManeuBuffer.objects.create(admin_id=admin_id, guest_id=guest_id, name=name, time=time, call=call, remark=remark, content=content)


def report_detail(admin_id='', id=''):
    return ManeuBuffer.objects.filter(admin_id=admin_id, id=id).first()


def report_update(id='', admin_id='', time='', name='', call='', content='', remark=''):
    return ManeuBuffer.objects.filter(id=id, admin_id=admin_id).update(name=name, time=time, call=call, remark=remark, content=content)
