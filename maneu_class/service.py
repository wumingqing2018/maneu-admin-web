from maneu.models import ManeuClass


def class_list(admin_id=''):
    return ManeuClass.objects.filter(admin_id=admin_id).all()


def class_insert(admin_id='', name='', series='', color='', price=''):
    return ManeuClass.objects.create(admin_id=admin_id, name=name, series=series, color=color, price=price)


def class_delete(admin_id='', id=''):
    return ManeuClass.objects.filter(admin_id=admin_id, id=id).delete()
