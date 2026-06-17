from maneu.models import ManeuOrderV2
from maneu.models import ManeuStore


def find_order_month(admin_id='', month='', year=''):
    return ManeuOrderV2.objects.filter(time__year=year, time__month=month, admin_id=admin_id).all()


def find_store_id(id=''):
    try:
        return ManeuStore.objects.filter(id=id).first()
    except BaseException as msg:
        print(msg)
        return None
