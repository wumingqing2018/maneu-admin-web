from django.db.models import Q

from maneu.models import ManeuAdmin
from maneu.models import ManeuOrder


def get_access_token(code=''):
    return ManeuAdmin.objects.filter(id=code).first()


def update_access_token(content):
    return ManeuAdmin.objects.all().update(content=content)


def order_detail(admin_id='', order_id=''):
    """
    查找指定订单
    根据时间排序
    """
    return ManeuOrder.objects.filter(id=order_id, admin_id=admin_id).first()


def order_delete(admin_id='', order_id=''):
    """
    查找指定订单a
    根据时间排序
    """
    return ManeuOrder.objects.filter(admin_id=admin_id, id=order_id).delete()


def order_search(admin_id='', timeS='', timeE='', value=''):
    return ManeuOrder.objects.filter(Q(name__icontains=value, admin_id=admin_id, time__gte=timeS, time__lte=timeE, ) | Q(phone__icontains=value, admin_id=admin_id, time__gte=timeS, time__lte=timeE, )).order_by('-time').all()



def order_insert(admin_id='', name='', time='', call='', content='', guest_id='', store_id='', report_id='', remark=''):
    return ManeuOrder.objects.create(name=name, time=time, phone=call, guest_id=guest_id, admin_id=admin_id,
                                     store_id=store_id, report_id=report_id, remark=remark, content=content)


def order_update(admin_id='', order_id='', name='', call='', time="", remark="", content=''):
    return ManeuOrder.objects.filter(id=order_id, admin_id=admin_id).update(name=name, phone=call, time=time,
                                                                            remark=remark, content=content)
