"""
maneu_admin/service.py

ManeuAdmin / ManeuReport 数据访问
"""

from django.db.models import Q

from maneu.models import ManeuAdmin, ManeuReport


def user_detail(index_id=''):
    """按主键查管理员，找不到返回 None"""
    if not index_id:
        return None
    return ManeuAdmin.objects.filter(id=index_id).first()


def user_update(index_id='', phone='', nickname='', location=''):
    """更新管理员资料（不含 password / content）"""
    if not index_id:
        return 0
    return ManeuAdmin.objects.filter(id=index_id).update(
        nickname=nickname,
        phone=phone,
        location=location,
    )


def report_search_time(admin_id='', timeS='', timeE=''):
    """按时间范围查报告（status=2）"""
    return (
        ManeuReport.objects
        .filter(admin_id=admin_id, time__gte=timeS, time__lte=timeE, status=2)
        .order_by('-time')
    )


def report_search_data(admin_id='', value=''):
    """按名称/手机号模糊查报告（status=2）"""
    return (
        ManeuReport.objects
        .filter(
            Q(admin_id=admin_id, name__icontains=value, status=2)
            | Q(admin_id=admin_id, phone__icontains=value, status=2)
        )
        .order_by('-time')
    )