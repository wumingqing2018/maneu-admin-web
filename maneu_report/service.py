"""
maneu_report/service.py

ManeuReport 数据访问
"""

from django.db.models import Q

from maneu.models import ManeuReport

# 所有允许更新/插入的报告字段
# 已补齐：sex / age / ot / em / dfh
_REPORT_FIELDS = [
    # 基础信息
    'name', 'time', 'phone', 'remark',
    'sex', 'age', 'ot', 'em', 'dfh',
    'plan', 'pd',

    # 右眼
    'od_al', 'od_ak', 'od_ax', 'od_ad', 'od_add', 'od_bc',
    'od_cyl', 'od_cct', 'od_va', 'od_sph', 'od_pr', 'od_fr',
    'od_lt', 'od_vt',

    # 左眼
    'os_al', 'os_ak', 'os_ax', 'os_ad', 'os_add', 'os_bc',
    'os_cyl', 'os_cct', 'os_va', 'os_sph', 'os_pr', 'os_fr',
    'os_lt', 'os_vt',
]


def report_insert(admin_id='', index_id='', status=0, content=None):
    """创建报告

    :param content: 需含 _REPORT_FIELDS 中的字段（缺失则忽略）
    :return: ManeuReport 实例
    """
    if not content:
        content = {}

    data = {f: content[f] for f in _REPORT_FIELDS if f in content}
    data.update(admin_id=admin_id, id=index_id, status=status)
    return ManeuReport.objects.create(**data)


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


def report_update(admin_id='', index_id='', content=None):
    """更新报告（只更新 content 里有的字段）"""
    if not admin_id or not index_id:
        return 0
    if not content:
        return 0

    update_data = {f: content[f] for f in _REPORT_FIELDS if f in content}
    if not update_data:
        return 0
    return ManeuReport.objects.filter(admin_id=admin_id, id=index_id).update(**update_data)


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
