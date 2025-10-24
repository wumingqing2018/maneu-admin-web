from django.db.models import Q

from maneu.models import ManeuBuffer


def report_index(admin_id='', start='', end=''):
    return ManeuBuffer.objects.filter(admin_id=admin_id, time__gte=start, time__lte=end).order_by('-time').all()


def report_search(admin_id, timeS, timeE, value):
    return ManeuBuffer.objects.filter(
        Q(name__icontains=value, admin_id=admin_id, time__gte=timeS, time__lte=timeE, ) | Q(phone__icontains=value,
                                                                                            admin_id=admin_id,
                                                                                            time__gte=timeS,
                                                                                            time__lte=timeE, )).order_by(
        '-time').all()


def report_delete(admin_id='', id=''):
    return ManeuBuffer.objects.filter(admin_id=admin_id, id=id).all().delete()


def report_insert(admin_id='', guest_id='', name='', time='', phone='', remark='', content=''):
    return ManeuBuffer.objects.create(admin_id=admin_id, guest_id=guest_id, name=name, time=time, phone=phone,
                                      remark=remark, plan=content['PLAN'],
                                      pd=content['PD'],
                                      od_al=content['OD_AL'],
                                      od_ak=content['OD_AK'],
                                      od_ax=content['OD_AX'],
                                      od_ad=content['OD_AD'],
                                      od_add=content['OD_ADD'],
                                      od_bc=content['OD_BC'],
                                      od_cyl=content['OD_CYL'],
                                      od_cct=content['OD_CCT'],
                                      od_va=content['OD_VA'],
                                      od_sph=content['OD_SPH'],
                                      od_pr=content['OD_PR'],
                                      od_fr=content['OD_FR'],
                                      od_lt=content['OD_LT'],
                                      od_vt=content['OD_VT'],
                                      os_al=content['OS_AL'],
                                      os_ak=content['OS_AK'],
                                      os_ad=content['OS_AD'],
                                      os_ax=content['OS_AX'],
                                      os_add=content['OS_ADD'],
                                      os_bc=content['OS_BC'],
                                      os_cyl=content['OS_CYL'],
                                      os_cct=content['OS_CCT'],
                                      os_va=content['OS_VA'],
                                      os_sph=content['OS_SPH'],
                                      os_pr=content['OS_PR'],
                                      os_fr=content['OS_FR'],
                                      os_lt=content['OS_LT'],
                                      os_vt=content['OS_VT'], )


def report_detail(admin_id='', id=''):
    return ManeuBuffer.objects.filter(admin_id=admin_id, id=id).first()


def report_update(id='', admin_id='', time='', name='', phone='', content='', remark=''):
    return ManeuBuffer.objects.filter(id=id, admin_id=admin_id).update(name=name, time=time, phone=phone, remark=remark,
                                                                       content=content)
