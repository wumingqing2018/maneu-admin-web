from maneu.models import ManeuAdmin


def find_user(admin_id):
    """
    通过admin_id查找用户
    """
    return ManeuAdmin.objects.filter(id=admin_id).first()


def find_user_all():
    """
    通过admin_id查找用户
    """
    return ManeuAdmin.objects.filter().all()


def find_user_username(username=''):
    """
    通过username查找用户
    """
    return ManeuAdmin.objects.filter(username=username).first()


def find_username_password(username, password):
    return ManeuAdmin.objects.filter(username=username, password=password).first()


def add_user(post):
    """添加用户"""
    try:
        return ManeuAdmin.objects.create(
            username=post['username'],
            password=post['password'],
            email=post['email'],
            phone=post['phone'],
            level='1',
            state='1',
        )
    except BaseException as msg:
        return str(msg)


def user_delete(admin_id):
    return ManeuAdmin.objects.filter(admin_id=admin_id).delete()


def user_update(old_password='', localtion='', admin_id='', nickname='', password='', email='', phone='', remark=''):
    try:
        ManeuAdmin.objects.filter(admin_id=admin_id, password=old_password).update(nickname=nickname, password=password,
                                                                                   email=email, phone=phone,
                                                                                   localtion=localtion,
                                                                                   remark=remark)
    except BaseException as msg:
        return str(msg)


def user_updata(username, password):
    try:
        ManeuAdmin.objects.filter(username=username).update(password=password)
    except BaseException as msg:
        return str(msg)


def user_insert(username='', nickname='', password='', email='', phone='', remark=''):
    try:
        return ManeuAdmin.objects.create(username=username, password=password, nickname=nickname, email=email,
                                         phone=phone, level=0, state=0, remark=remark)
    except BaseException as msg:
        return str(msg)
