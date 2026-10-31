"""
maneu_report/service.py

ManeuReport 数据访问
"""

from django.db.models import Q

from maneu.models import ManeuReport


_REPORT_FIELDS = [
    # 基础信息
    'name', 'phone', 'remark','content'
]


def report_insert(admin_id='', index_id='', time='', name='', phone='', remark='', content=None):
    """创建报告

    :param content: 需含 _REPORT_FIELDS 中的字段（缺失则忽略）
    :return: ManeuReport 实例
    """
    return ManeuReport.objects.create(admin_id=admin_id, id=index_id, time=time, name=name, phone=phone, remark=remark, content=content)


def report_detail(admin_id='', index_id=''):
    """查报告，找不到返回 None"""
    if not admin_id or not index_id:
        return None
    return ManeuReport.objects.filter(admin_id=admin_id, id=index_id).first()


def report_delete(admin_id='', index_id=''):
    """删除报告，返回 (删除数量, 明细)"""
    if not admin_id or not index_id:
        return 0, {}
    return ManeuReport.objects.filter(admin_id=admin_id, id=index_id).delete()


def report_update(admin_id='', index_id='', name='', phone='', remark='', content=None):
    """更新报告（只更新 content 里有的字段）"""
    if not admin_id or not index_id:
        return 0
    if not content:
        return 0

    return ManeuReport.objects.filter(admin_id=admin_id, id=index_id).update(name=name, phone=phone, remark=remark, content=content)


def report_search_time(admin_id='', timeS='', timeE=''):
    """按时间范围查报告 """
    return (
        ManeuReport.objects
        .filter(admin_id=admin_id, time__gte=timeS, time__lte=timeE)
        .order_by('-time')
    )


def report_search_data(admin_id='', value=''):
    """按名称/手机号模糊查报告 """
    return (
        ManeuReport.objects
        .filter(
            Q(admin_id=admin_id, name__icontains=value)
            | Q(admin_id=admin_id, phone__icontains=value)
        )
        .order_by('-time')
    )
