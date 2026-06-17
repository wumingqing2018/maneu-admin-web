from maneu.models import ManeuOrderV1


def batch_admin_id(admin_id='', time=''):
    return ManeuOrderV1.objects.filter(admin_id=admin_id, time=time).order_by('-time').all()


def batch_list():
    return ManeuOrderV1.objects.order_by('-time').all()


def batch_list_ByName(arg):
    return ManeuOrderV1.objects.filter(name=arg).order_by('-time').all()


def batch_list_ByPhone(arg):
    return ManeuOrderV1.objects.filter(phone=arg).order_by('-time').all()


def batch_detail(id=''):
    return ManeuOrderV1.objects.filter(id=id).first()


def batch_insert(form, order, order_id):
    try:
        ManeuOrderV1.objects.create(
            order_id=order_id,
            name=form['name'],
            phone=form['phone'],
            order=order,
            remark=form['remark'],
        )
        return True
    except BaseException as msg:
        print(msg)
        return False


def batch_delete(id=''):
    return ManeuOrderV1.objects.filter(id=id).all().delete()


def find_batch_date(date=''):
    try:
        return ManeuOrderV1.objects.filter(time__gt=date).all()
    except BaseException as msg:
        print(msg)
        return None
