"""
maneu_admin/api.py

管理员资料 + 报告查询
"""

import logging

from django.http import JsonResponse

from common.util_jwt import get_admin_id
from common.util_verify import is_uuid      # 保留（可能别处还要用）
from maneu_admin.service import (
    user_detail,
    user_update,
    report_search_time,
    report_search_data,
)

logger = logging.getLogger(__name__)


# ============================================================
# 工具
# ============================================================
def _json_error(message, status=400):
    return JsonResponse(
        {'status': False, 'message': message, 'content': {}},
        status=status,
    )


def _json_ok(content=None, message=''):
    return JsonResponse({
        'status': True,
        'message': message,
        'content': content or {},
    })


# ============================================================
# 管理员资料
# ============================================================
def index(request):
    """获取当前登录管理员资料（只能查自己）"""
    admin_id = get_admin_id(request)
    if not admin_id:
        return _json_error('未登录或登录已过期', status=401)

    try:
        user = user_detail(index_id=admin_id)
    except Exception:
        logger.exception('查询管理员资料失败 admin_id=%s', admin_id)
        return _json_error('系统错误', status=500)

    if not user:
        return _json_error('管理员不存在', status=404)

    return _json_ok({
        'nickname': user.nickname,
        'location': user.location,
        'phone':    user.phone,
        'time':     user.time,
    })


def update(request):
    """更新当前登录管理员资料（只能改自己）"""
    admin_id = get_admin_id(request)
    if not admin_id:
        return _json_error('未登录或登录已过期', status=401)

    phone    = (request.POST.get('phone')    or '').strip()
    nickname = (request.POST.get('nickname') or '').strip()
    location = (request.POST.get('location') or '').strip()

    if not nickname:
        return _json_error('昵称不能为空')

    try:
        user_update(
            index_id=admin_id,
            phone=phone,
            nickname=nickname,
            location=location,
        )
    except Exception:
        logger.exception('更新管理员资料失败 admin_id=%s', admin_id)
        return _json_error('系统错误', status=500)

    return _json_ok({}, '更新成功')


# ============================================================
# 报告查询
# ============================================================
def search_time(request):
    """按时间范围查报告"""
    admin_id = get_admin_id(request)
    if not admin_id:
        return _json_error('未登录或登录已过期', status=401)

    timeS = request.POST.get('timeS')
    timeE = request.POST.get('timeE')
    if not timeS or not timeE:
        return _json_error('请提供起始和结束时间')

    try:
        data = report_search_time(admin_id=admin_id, timeS=timeS, timeE=timeE)
        return _json_ok(list(data.values('id', 'name', 'phone', 'time', 'remark')))
    except Exception:
        logger.exception('查询报告失败 admin_id=%s', admin_id)
        return _json_error('系统错误', status=500)


def search_data(request):
    """按关键词查报告"""
    admin_id = get_admin_id(request)
    if not admin_id:
        return _json_error('未登录或登录已过期', status=401)

    value = (request.POST.get('value') or '').strip()
    if not value:
        return _json_error('请输入搜索关键词')

    try:
        data = report_search_data(admin_id=admin_id, value=value)
        return _json_ok(list(data.values('id', 'name', 'phone', 'time', 'remark')))
    except Exception:
        logger.exception('查询报告失败 admin_id=%s', admin_id)
        return _json_error('系统错误', status=500)