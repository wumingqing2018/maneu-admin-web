from maneu.models import ManeuAdmin


def get_wx_to():
    return ManeuAdmin.objects.filter().first()


def find_username_password(username, password):
    return ManeuAdmin.objects.filter(username=username, password=password).first()


def user_update(admin_id='', phone='', nickname='', location='', content=''):
    return ManeuAdmin.objects.filter(id=admin_id).update(nickname=nickname, phone=phone, location=location,
                                                         content=content)


def user_insert(username='', nickname='', password='', email='', phone=''):
    return ManeuAdmin.objects.create(username=username, password=password, nickname=nickname, email=email,
                                     phone=phone, level=0, state=0)


def user_detail(admin_id=''):
    return ManeuAdmin.objects.filter(id=admin_id).first()


def admin_update(level='', state=''):
    return ManeuAdmin.objects.all().update(level=level, state=state)
