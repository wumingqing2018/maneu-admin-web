from maneu.models import ManeuService


def ManeuService_orderID(order_id=''):
    return ManeuService.objects.filter(order_id=order_id).order_by('-time').all()


def ManeuService_insert(order_id='', content=''):
    return ManeuService.objects.create(order_id=order_id, content=content)


def ManeuService_delete_order_id(order_id=''):
    return ManeuService.objects.filter(order_id=order_id).all().delete()


def ManeuService_delete_id(id=''):
    return ManeuService.objects.filter(id=id).all().delete()


def ManeuService_index(time=''):
    return ManeuService.objects.filter(time=time).order_by('-time').all()
