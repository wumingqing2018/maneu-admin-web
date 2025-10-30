from django.db.models import Q

from maneu.models import ManeuBuffer


def report_index(admin_id='', start='', end=''):
    return ManeuBuffer.objects.filter(admin_id=admin_id, time__gte=start, time__lte=end).order_by('-time').all()


def report_search_text(admin_id='', value=''):
    return ManeuBuffer.objects.filter(
        Q(name__icontains=value, admin_id=admin_id) | Q(phone__icontains=value, admin_id=admin_id)).order_by(
        '-time').all()


def report_search_time(admin_id='', timeS='', timeE=''):
    return ManeuBuffer.objects.filter(admin_id=admin_id, time__gte=timeS, time__lte=timeE).order_by('-time').all()


def report_delete(admin_id='', id=''):
    return ManeuBuffer.objects.filter(admin_id=admin_id, id=id).all().delete()


def report_insert(admin_id='', guest_id='', name='', time='', phone='', remark='', content=''):
    return ManeuBuffer.objects.create(admin_id=admin_id, guest_id=guest_id, name=name, time=time, phone=phone,
                                      remark=remark, plan=content['plan'],
                                      pd=content['pd'],
                                      os_al=content['os_al'],
                                      os_ak=content['os_ak'],
                                      os_ax=content['os_ax'],
                                      os_ad=content['os_ad'],
                                      os_add=content['os_add'],
                                      os_bc=content['os_bc'],
                                      os_cyl=content['os_cyl'],
                                      os_cct=content['os_cct'],
                                      os_va=content['os_va'],
                                      os_sph=content['os_sph'],
                                      os_pr=content['os_pr'],
                                      os_fr=content['os_pr'],
                                      os_lt=content['os_lt'],
                                      os_vt=content['os_vt'],

                                      od_al=content['od_al'],
                                      od_ak=content['od_ak'],
                                      od_ax=content['od_ax'],
                                      od_ad=content['od_ad'],
                                      od_add=content['od_add'],
                                      od_bc=content['od_bc'],
                                      od_cyl=content['od_cyl'],
                                      od_cct=content['od_cct'],
                                      od_va=content['od_va'],
                                      od_sph=content['od_sph'],
                                      od_pr=content['od_pr'],
                                      od_fr=content['od_pr'],
                                      od_lt=content['od_lt'],
                                      od_vt=content['od_vt'],
                                      )


def report_detail(admin_id='', id=''):
    return ManeuBuffer.objects.filter(admin_id=admin_id, id=id).first()


def report_update(id='', admin_id='', time='', name='', phone='', content='', remark=''):
    return ManeuBuffer.objects.filter(id=id, admin_id=admin_id).update(name=name, time=time, phone=phone, remark=remark,
                                                                       content=content)
