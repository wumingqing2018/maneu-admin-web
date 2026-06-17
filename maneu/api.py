"""
认证视图模块
包含：短信验证码发送、access_token 获取（登录）、refresh_token 刷新、移除 token（登出）
"""

import logging
from django.http import JsonResponse

from common import common
from common.jwt_util import generate_access_token, generate_refresh_token, verify_token
from common.verify import is_call, is_code
from maneu import service

logger = logging.getLogger(__name__)


def sendsms(request):
    """
    发送短信验证码
    GET 参数：
        call - 手机号码
    返回：
        JSON {status, message, content}
    """
    phone_number = is_call(request.GET.get('call'))

    if not phone_number:
        return JsonResponse({
            'status': False,
            'message': '请输入正确的手机号码',
            'content': {}
        })

    # 检查账号是否存在
    if not service.admin_exist(call=phone_number):  # 假设存在此方法，避免对未注册手机发送
        return JsonResponse({
            'status': False,
            'message': '该手机号尚未注册，请先联系管理员',
            'content': {}
        })

    # 生成随机验证码
    code = common.get_random_code()

    # 调用短信发送接口
    send_result = service.sendsms(call=phone_number, code=code)
    if not send_result or send_result.get('Code') != 'OK':
        logger.warning(f"短信发送失败：手机号 {phone_number}, 响应 {send_result}")
        return JsonResponse({
            'status': False,
            'message': '短信发送失败，请稍后重试',
            'content': {}
        })

    # 发送成功（code 可根据需求缓存至 redis/数据库，生产环境不应返回给前端）
    return JsonResponse({
        'status': True,
        'message': '验证码已发送',
        'content': {}  # 注意：线上环境不应返回 code
    })


def access_token(request):
    """
    登录接口：使用手机号 + 验证码换取 access_token 和 refresh_token
    GET 参数：
        call - 手机号
        code - 验证码
    返回：
        JSON {status, message, content: {access_token, refresh_token}}
    """
    call = is_call(request.GET.get('call'))
    code = is_code(request.GET.get('code'))

    # 参数校验
    if not call or not code:
        return JsonResponse({
            'status': False,
            'message': '请填写手机号和验证码',
            'content': {}
        })

    # 验证码登录验证
    admin_user = service.admin_login(call=call, code=code)
    if not admin_user:
        return JsonResponse({
            'status': False,
            'message': '验证码错误或手机号未注册',
            'content': {}
        })

    # 签发双 token
    try:
        a_token = generate_access_token(admin_user)
        r_token = generate_refresh_token(admin_user)
    except Exception as e:
        logger.error(f"生成 Token 异常：{e}")
        return JsonResponse({
            'status': False,
            'message': '系统异常，请稍后重试',
            'content': {}
        })

    return JsonResponse({
        'status': True,
        'message': '登录成功',
        'content': {
            'access_token': a_token,
            'refresh_token': r_token
        }
    })


def refresh_token(request):
    """
    刷新 access_token 接口
    GET 参数：
        refresh_token - 刷新令牌
    返回：
        JSON {status, access_token} 或 401 错误
    注意：
        - 刷新令牌应通过安全渠道传递（此处为演示使用 GET）
        - 可启用滚动刷新，同时更新 refresh_token
    """
    token = request.GET.get('refresh_token')
    if not token:
        return JsonResponse({
            'status': False,
            'message': '缺少 refresh_token'
        }, status=401)

    # 验证 refresh_token 的有效性和类型
    payload = verify_token(token, expected_type='refresh')
    if not payload:
        return JsonResponse({
            'status': False,
            'message': 'refresh_token 无效或已过期'
        }, status=401)

    # 根据 token 中的用户 ID 获取用户对象
    user_id = payload.get('user_id')
    if not user_id:
        return JsonResponse({
            'status': False,
            'message': 'Token 数据异常'
        }, status=401)

    user = service.admin_find_id(user_id)
    if not user:
        logger.warning(f"刷新 token 失败，用户不存在：{user_id}")
        return JsonResponse({
            'status': False,
            'message': '用户不存在或已被禁用'
        }, status=401)

    # 生成新的 access_token（可同时刷新 refresh_token 实现滚动刷新）
    try:
        new_access_token = generate_access_token(user)
        # new_refresh_token = generate_refresh_token(user)  # 滚动刷新时取消注释
    except Exception as e:
        logger.error(f"刷新 token 异常：{e}")
        return JsonResponse({
            'status': False,
            'message': '系统异常，请稍后重试'
        }, status=500)

    response_data = {
        'status': True,
        'message': '刷新成功',
        'access_token': new_access_token,
        # 'refresh_token': new_refresh_token,
    }
    return JsonResponse(response_data)


def remove_token(request):
    """
    登出接口（客户端主动清除 token）
    由于 JWT 是无状态的，服务端只需返回成功，由客户端删除本地存储的 token 即可。
    如需实现服务端 token 吊销，需引入黑名单（如 redis）。
    """
    # 可选：将当前 access_token 加入黑名单（需从 Authorization 头获取）
    return JsonResponse({
        'status': True,
        'message': '已退出登录',
        'content': {}
    })