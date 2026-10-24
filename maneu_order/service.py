"""
maneu_order/service.py

ManeuOrder 数据访问
"""

import json

from django.db.models import Q

from maneu.models import ManeuOrder


def _dump_products(products):
    """把 products list 序列化成 JSON 字符串"""
    if products is None:
        return '[]'
    if isinstance(products, str):
        # 已经是 JSON 字符串，直接存
        return products
    return json.dumps(products, ensure_ascii=False)


def order_insert(admin_id='', index_id='', status=3, content=None):
    """
    创建订单

    content 需包含：name / time / phone / remark / products
    """
    if not content:
        content = {}

    return ManeuOrder.objects.create(
        id=index_id,
        admin_id=admin_id,
        status=status,
        name=content.get('name', ''),
        time=content.get('time'),
        phone=content.get('phone', ''),
        remark=content.get('remark', ''),
        content=_dump_products(content.get('products')),
    )


def order_delete(admin_id='', index_id=''):
    """删除订单，返回 (删除数量, 明细)"""
    if not admin_id or not index_id:
        return 0, {}
    return ManeuOrder.objects.filter(admin_id=admin_id, id=index_id).delete()


def order_detail(admin_id='', index_id=''):
    """查订单，找不到返回 None"""
    if not admin_id or not index_id:
        return None
    return ManeuOrder.objects.filter(admin_id=admin_id, id=index_id).first()


def order_search_time(admin_id='', timeS='', timeE=''):
    """按时间范围查订单"""
    return (
        ManeuOrder.objects
        .filter(admin_id=admin_id, time__gte=timeS, time__lte=timeE)
        .order_by('-time')
    )


def order_search_data(admin_id='', value=''):
    """按名称/手机号模糊查订单"""
    return (
        ManeuOrder.objects
        .filter(
            Q(name__icontains=value, admin_id=admin_id)
            | Q(phone__icontains=value, admin_id=admin_id)
        )
        .order_by('-time')
    )


def order_update_data(admin_id='', index_id='', content=None):
    """
    更新订单（只更新 remark 和 products）
    """
    if not content:
        content = {}
    return ManeuOrder.objects.filter(admin_id=admin_id, id=index_id).update(
        remark=content.get('remark', ''),
        content=_dump_products(content.get('products')),
    )