"""
maneu/service.py

ManeuAdmin 数据访问

约定：
    - ManeuAdmin.username 字段存的是手机号
    - 所有查询找不到返回 None，不抛异常
"""

import logging

from maneu.models import ManeuAdmin

logger = logging.getLogger(__name__)


def admin_find_id(code=''):
    """按主键查管理员，找不到返回 None"""
    if not code:
        return None
    return ManeuAdmin.objects.filter(id=code).first()


def admin_find_username(code=''):
    """按 username（手机号）查管理员，找不到返回 None"""
    if not code:
        return None
    return ManeuAdmin.objects.filter(username=code).first()