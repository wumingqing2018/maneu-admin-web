from django.db.models import Q

from maneu.models import ManeuStore


def store_update(admin_id='', index_id='', content=''):
    return ManeuStore.objects.filter(admin_id=admin_id, id=index_id).update(content=content)


def store_insert(admin_id='', index_id='', name='', time='', phone='', status='', remark='', content=''):
    return ManeuStore.objects.create(id=index_id, admin_id=admin_id, time=time, name=name, phone=phone, status=status, remark=remark, content=content)


def store_delete(admin_id='', index_id=''):
    return ManeuStore.objects.filter(admin_id=admin_id, id=index_id).delete()


def store_detail(admin_id='', index_id=''):
    return ManeuStore.objects.filter(admin_id=admin_id, id=index_id).first()


def store_search_time(admin_id='', timeS='', timeE=''):
    return ManeuStore.objects.filter(admin_id=admin_id, time__gte=timeS, time__lte=timeE).order_by('-time').all()


def store_search_data(admin_id='', value=''):
    return ManeuStore.objects.filter(Q(name__icontains=value, admin_id=admin_id) | Q(phone__icontains=value, admin_id=admin_id)).order_by('-time').all()
