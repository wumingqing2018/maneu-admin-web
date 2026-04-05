from django.db.models import Q

from maneu.models import ManeuReport


def report_update(admin_id='', index_id='', content=''):
    return ManeuReport.objects.filter(admin_id=admin_id, id=index_id).update(os_al=content['os_al'],
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

                                                                             plan=content['plan'],
                                                                             pd=content['pd'])


def report_insert(admin_id='', index_id='', name='', time='', phone='', status='', remark='', content=''):
    return ManeuReport.objects.create(admin_id=admin_id,
                                      id=index_id,
                                      name=name,
                                      time=time,
                                      phone=phone,
                                      status=status,
                                      remark=remark,

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

                                      plan=content['plan'],
                                      pd=content['pd'])


def report_detail(admin_id='', index_id=''):
    return ManeuReport.objects.filter(admin_id=admin_id, id=index_id).first()


def report_delete(admin_id='', index_id=''):
    return ManeuReport.objects.filter(admin_id=admin_id, id=index_id).first().delete()


def report_search_time(admin_id='', timeS='', timeE=''):
    return ManeuReport.objects.filter(admin_id=admin_id, time__gte=timeS, time__lte=timeE, status=2).order_by('-time').all()


def report_search_data(admin_id='', value=''):
    return ManeuReport.objects.filter(Q(admin_id=admin_id, name__icontains=value,status=2) | Q(admin_id=admin_id, phone__icontains=value,status=2)).order_by('-time').all()