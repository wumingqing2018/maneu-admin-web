"""
maneu/api.py

认证相关 API
- 发送短信验证码
- 短信验证码登录
- 刷新 access_token
- 前端登出
- 测试接口：免密登录（仅 DEBUG + 本地 IP 可用）
"""

import logging
import random

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from common.util_jwt import (
    generate_access_token,
    generate_refresh_token,
    verify_token,
)
from common.util_sms import send_sms
from common.util_verify import is_call, is_code
from maneu import service

logger = logging.getLogger(__name__)


# ============================================================
# 常量
# ============================================================
SMS_CODE_PREFIX  = 'sms:code:'
SMS_LIMIT_PREFIX = 'sms:limit:'
SMS_CODE_TTL     = 300
SMS_LIMIT_TTL    = 60

# test_login 只允许本机访问（生产环境即使误开 DEBUG 也拦住）
TEST_LOGIN_ALLOWED_IPS = ('127.0.0.1', '::1', 'localhost')


# ============================================================
# 工具
# ============================================================
def _json_error(message, status=400):
    return JsonResponse(
        {'status': False, 'message': message, 'content': {}},
        status=status,
    )


def _json_ok(content=None, message='请求成功'):
    return JsonResponse({
        'status': True,
        'message': message,
        'content': content or {},
    })


def _client_ip(request):
    """取客户端真实 IP（兼容反向代理）"""
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


# ============================================================
# 发送短信验证码
# ============================================================
@csrf_exempt
@require_http_methods(["POST"])
def sendsms(request):
    """发送短信验证码（服务端生成，60 秒限流）"""
    call = (request.POST.get('call') or '').strip()

    if not is_call(call):
        return _json_error('请输入正确的手机号')

    limit_key = f'{SMS_LIMIT_PREFIX}{call}'
    if cache.get(limit_key):
        return _json_error('发送过于频繁，请 60 秒后再试')

    try:
        user = service.admin_find_username(code=call)
    except Exception:
        logger.exception('查询用户失败 call=%s', call)
        return _json_error('系统繁忙，请稍后重试', status=500)

    if not user:
        return _json_error('该手机号未注册')

    code = f'{random.randint(0, 999999):06d}'

    cache.set(f'{SMS_CODE_PREFIX}{call}', code, timeout=SMS_CODE_TTL)
    cache.set(limit_key, 1, timeout=SMS_LIMIT_TTL)

    result = send_sms(call, code)
    if result.get('Code') == 'OK':
        logger.info('短信已发送 call=%s', call)
        return _json_ok({}, '验证码已发送')

    logger.warning('短信发送失败 call=%s result=%s', call, result)
    cache.delete(f'{SMS_CODE_PREFIX}{call}')
    cache.delete(limit_key)
    return _json_error(result.get('Message', '发送失败'), status=500)


# ============================================================
# 短信验证码登录
# ============================================================
@csrf_exempt
@require_http_methods(["POST"])
def access_token(request):
    """短信验证码登录（一次性）"""
    call = (request.POST.get('call') or '').strip()
    code = (request.POST.get('code') or '').strip()

    if not is_call(call):
        return _json_error('请输入正确的手机号')
    if not is_code(code):
        return _json_error('请输入 6 位数字验证码')

    cached_code = cache.get(f'{SMS_CODE_PREFIX}{call}')
    if not cached_code or str(cached_code) != str(code):
        return _json_error('验证码错误或已过期')

    cache.delete(f'{SMS_CODE_PREFIX}{call}')

    user = service.admin_find_username(code=call)
    if not user:
        return _json_error('该手机号未注册', status=401)
    if not getattr(user, 'is_active', True):
        return _json_error('账号已被禁用', status=403)

    try:
        a_token = generate_access_token(user)
        r_token = generate_refresh_token(user)
    except Exception:
        logger.exception('生成 JWT 失败 phone=%s', call)
        return _json_error('系统错误', status=500)

    logger.info('用户登录成功 phone=%s', call)

    return _json_ok(
        {'access_token': a_token, 'refresh_token': r_token},
        '登录成功',
    )


# ============================================================
# 刷新
# ============================================================
@csrf_exempt
@require_http_methods(["POST"])
def refresh_token(request):
    """用 refresh_token 换新的 access_token"""
    token = request.POST.get('refresh_token')
    if not token:
        return _json_error('缺少 refresh_token', status=401)

    payload = verify_token(token, expected_type='refresh')
    if not payload:
        return _json_error('refresh_token 无效或已过期', status=401)

    user_id = payload.get('user_id')
    if not user_id:
        return _json_error('refresh_token 中缺少 user_id', status=401)

    user = service.admin_find_id(user_id)
    if not user:
        return _json_error('用户不存在', status=401)

    try:
        new_access_token = generate_access_token(user)
    except Exception:
        logger.exception('生成 JWT 失败 user_id=%s', user_id)
        return _json_error('系统错误', status=500)

    return _json_ok({'access_token': new_access_token}, '刷新成功')


# ============================================================
# 登出
# ============================================================
@csrf_exempt
@require_http_methods(["POST"])
def remove_token(request):
    """前端登出（无状态 JWT）"""
    return _json_ok({}, 'OK')


# ============================================================
# 测试接口：免密登录
# ============================================================
@csrf_exempt
@require_http_methods(["POST"])
def test_login(request):
    """
    ⚠️ 测试接口：免密登录

    双重保护：
        1. 必须 settings.DEBUG = True
        2. 必须来自本机（127.0.0.1 / ::1）
    """
    if not settings.DEBUG:
        return _json_error('测试接口已禁用', status=403)

    ip = _client_ip(request)
    if ip not in TEST_LOGIN_ALLOWED_IPS:
        logger.warning('test_login 拒绝非本地访问 ip=%s', ip)
        return _json_error('测试接口只允许本地访问', status=403)

    call = (request.POST.get('call') or '').strip()

    if not is_call(call):
        return _json_error('请输入正确的手机号')

    user = service.admin_find_username(code=call)
    if not user:
        return _json_error('该手机号未注册', status=401)
    if not getattr(user, 'is_active', True):
        return _json_error('账号已被禁用', status=403)

    try:
        a_token = generate_access_token(user)
        r_token = generate_refresh_token(user)
    except Exception:
        logger.exception('生成 JWT 失败 phone=%s', call)
        return _json_error('系统错误', status=500)

    logger.warning('⚠️ 免密测试登录 phone=%s ip=%s', call, ip)

    return _json_ok(
        {
            'access_token': a_token,
            'refresh_token': r_token,
            'warning': '此接口仅用于测试，生产环境已禁用',
        },
        '测试登录成功',
    )