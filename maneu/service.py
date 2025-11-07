from maneu.models import ManeuAdmin


def sendsms(call='', code=''):
    return ManeuAdmin.objects.filter(username=call).update(password=code)


def admin_login(call='', code='', mark=''):
    return ManeuAdmin.objects.filter(username=call, password=code).update(password=mark)


def admin_logout(id=''):
    return ManeuAdmin.objects.filter(id=id).update(password='')
