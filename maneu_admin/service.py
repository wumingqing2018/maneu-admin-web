from django.db.models import Q

from maneu.models import ManeuAdmin
from maneu.models import ManeuReport


def find_username_password(username, password):
    return ManeuAdmin.objects.filter(username=username, password=password).first()


def user_update(index_id='', phone='', nickname='', location='', content=''):
    return ManeuAdmin.objects.filter(id=index_id).update(nickname=nickname, phone=phone, location=location,
                                                         content=content)


def user_insert(username='', nickname='', password='', email='', phone=''):
    return ManeuAdmin.objects.create(username=username, password=password, nickname=nickname, email=email, phone=phone,
                                     level=0, state=0)


def user_detail(index_id=''):
    return ManeuAdmin.objects.filter(id=index_id).first()


def report_search_time(admin_id='', timeS='', timeE=''):
    return ManeuReport.objects.filter(admin_id=admin_id, time__gte=timeS, time__lte=timeE, status=2).order_by(
        '-time').all()


def report_search_data(admin_id='', value=''):
    return ManeuReport.objects.filter(
        Q(admin_id=admin_id, name__icontains=value, status=2) | Q(admin_id=admin_id, phone__icontains=value,
                                                                  status=2)).order_by('-time').all()
