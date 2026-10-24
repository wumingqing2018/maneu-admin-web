"""
common/util_jwt.py

JWT 工具
- 生成 access_token / refresh_token
- 校验 token
- 从 request 读取 admin_id

约定：
    - token 均携带 iss / type / iat / exp
    - 时间统一 UTC aware datetime，避免时区漂移
    - 兼容 PyJWT 1.x（bytes）和 2.x（str）
"""

from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings

from common.util_verify import is_uuid


# ============================================================
# 配置
# ============================================================
JWT_SECRET       = settings.JWT_CONFIG['SECRET_KEY']
JWT_ALGORITHM    = settings.JWT_CONFIG['ALGORITHM']
JWT_ISSUER       = settings.JWT_CONFIG.get('ISSUER', 'maneu')
ACCESS_LIFETIME  = settings.JWT_CONFIG['ACCESS_TOKEN_LIFETIME']
REFRESH_LIFETIME = settings.JWT_CONFIG.get('REFRESH_TOKEN_LIFETIME', 60 * 60 * 24 * 7)


# ============================================================
# 内部工具
# ============================================================
def _now():
    """当前 UTC aware datetime"""
    return datetime.now(timezone.utc)


def _encode(payload):
    """统一编码，兼容 PyJWT 1.x（bytes）和 2.x（str）"""
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


# ============================================================
# 生成
# ============================================================
def generate_access_token(user):
    """生成 Access Token"""
    now = _now()
    return _encode({
        'user_id': str(user.id),
        'type':    'access',
        'iss':     JWT_ISSUER,
        'exp':     now + timedelta(seconds=ACCESS_LIFETIME),
        'iat':     now,
    })


def generate_refresh_token(user):
    """生成 Refresh Token"""
    now = _now()
    return _encode({
        'user_id': str(user.id),
        'type':    'refresh',
        'iss':     JWT_ISSUER,
        'exp':     now + timedelta(seconds=REFRESH_LIFETIME),
        'iat':     now,
    })


# ============================================================
# 校验
# ============================================================
def verify_token(token, expected_type=None):
    """
    验证 JWT，成功返回 payload，失败返回 None。

    :param token: JWT 字符串
    :param expected_type: 'access' 或 'refresh'，用于限制用途
    :return: payload dict 或 None
    """
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            issuer=JWT_ISSUER,
        )
        if expected_type and payload.get('type') != expected_type:
            return None
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


# ============================================================
# request 辅助
# ============================================================
def get_admin_id(request):
    """
    从 request 获取 admin_id（UserMiddleware 挂载的 request.jwt_user_id）

    :return: UUID 字符串或 None
    """
    admin_id = getattr(request, 'jwt_user_id', None)
    if admin_id and is_uuid(admin_id):
        return admin_id
    return None