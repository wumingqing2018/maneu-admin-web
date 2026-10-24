"""
maneu_store/service.py

ManeuStore 数据访问
"""

from django.db.models import Q

from maneu.models import ManeuStore


def store_insert(admin_id='', index_id='', status=1, content=None):
    """
    创建零售记录

    :param content: dict，包含 time / name / phone / remark / content(JSON 字符串)
    :return: ManeuStore 实例
    """
    if not content:
        content = {}

    return ManeuStore.objects.create(
        id=index_id,
        admin_id=admin_id,
        time=content.get('time'),
        name=content.get('name', ''),
        phone=content.get('phone', ''),
        status=status,
        remark=content.get('remark', ''),
        content=content.get('content', ''),
    )


def store_delete(admin_id='', index_id=''):
    """
    删除零售记录

    :return: (删除数量, 明细) —— 不存在时返回 (0, {})
    """
    if not admin_id or not index_id:
        return 0, {}
    return ManeuStore.objects.filter(admin_id=admin_id, id=index_id).delete()


def store_detail(admin_id='', index_id=''):
    """查零售记录，找不到返回 None"""
    if not admin_id or not index_id:
        return None
    return ManeuStore.objects.filter(admin_id=admin_id, id=index_id).first()


def store_search_time(admin_id='', timeS='', timeE=''):
    """按时间范围查零售（status=1）"""
    return (
        ManeuStore.objects
        .filter(admin_id=admin_id, time__gte=timeS, time__lte=timeE)
        .order_by('-time')
    )


def store_search_data(admin_id='', value=''):
    """按名称/手机号模糊查零售（status=1）"""
    return (
        ManeuStore.objects
        .filter(
            Q(admin_id=admin_id, name__icontains=value)
            | Q(admin_id=admin_id, phone__icontains=value)
        )
        .order_by('-time')
    )


def store_update_fields(admin_id='', index_id='', fields=None):
    """
    部分更新零售记录（支持任意字段）

    :param fields: dict，可包含 name / phone / remark / content 等
    :return: 影响行数
    """
    if not admin_id or not index_id:
        return 0
    if not fields:
        return 0
    return ManeuStore.objects.filter(admin_id=admin_id, id=index_id).update(**fields)