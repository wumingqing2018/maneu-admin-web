from maneu.models import ManeuAdmin

def get_access_token(code=''):
    return ManeuAdmin.objects.filter(id=code).first()


def update_access_token(content):
    return ManeuAdmin.objects.all().update(content=content)


def sendsms(call='', code=''):
    return ManeuAdmin.objects.filter(username=call).update(password=code)


def admin_login(call='', code='', mark=''):
    return ManeuAdmin.objects.filter(username=call, code=code).update(password=mark)


def admin_logout(id=''):
    return ManeuAdmin.objects.filter(id=id).update(password='')
