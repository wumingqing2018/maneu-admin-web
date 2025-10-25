from maneu.models import ManeuAdmin


def sendsms(call='', code=''):
    return ManeuAdmin.objects.filter(phone=call).update(password=code)


def admin_login(call='', code=''):
    return ManeuAdmin.objects.filter(phone=call, password=code).first()


def admin_logout(id=''):
    return ManeuAdmin.objects.filter(id=id).update(password='')
