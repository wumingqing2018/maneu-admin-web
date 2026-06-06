from uuid import uuid4

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from common.verify import is_uuid
from maneu.models import ManeuAdmin


class UserMiddleware(MiddlewareMixin):
    """
    用户登录校验中间件。

    功能：
    1. 对以 '/maneu_' 开头的请求路径进行登录校验。
    2. 从 Cookie 中获取名为 'mark' 的令牌，验证是否为有效的 UUID 格式。
    3. 使用该令牌作为查询条件，在 ManeuAdmin 表的 password 字段中匹配用户记录。
    4. 若匹配成功，生成新的 UUID 令牌更新用户 password，并将新令牌存入 session 和 Cookie；
       否则重定向到登录页。

    ⚠️ 注意：此设计将用户 password 字段复用为临时令牌存储，会覆盖原有密码哈希，
              导致正常的密码登录失效，存在严重安全隐患。建议重构为独立的 token 字段。
    """

    # 需要校验的 URL 路径前缀
    PROTECTED_PREFIX = '/maneu_'
    # Cookie 中存储令牌的键名
    COOKIE_NAME = 'mark'
    # Cookie 有效期（秒）
    COOKIE_MAX_AGE = 3600
    # Session 中存储用户 ID 和令牌的键名
    SESSION_USER_ID_KEY = 'id'
    SESSION_TOKEN_KEY = 'mark'

    def __init__(self, get_response):
        self.get_response = get_response
        print("--用户登录校验中间件启动--")

    def process_request(self, request):
        """
        在请求处理前校验用户登录状态。
        若访问受保护路径且校验失败，则重定向到登录页面。
        """
        # 只处理受保护的路径前缀
        if not request.path.startswith(self.PROTECTED_PREFIX):
            return None  # 放行非保护路径

        # 1. 获取 Cookie 中的令牌
        token = request.COOKIES.get(self.COOKIE_NAME)
        if not token:
            return redirect('login')  # 无令牌，未登录

        # 2. 校验令牌格式（必须是有效的 UUID）
        if not is_uuid(token):
            return redirect('login')  # 格式错误，非法令牌

        # 3. 根据令牌（存储在 password 字段）查询用户
        try:
            admin = ManeuAdmin.objects.get(password=token)
        except ManeuAdmin.DoesNotExist:
            return redirect('login')  # 令牌无效或用户不存在

        # 4. 生成新令牌并更新用户 password 字段（原令牌作废）
        new_token = str(uuid4())
        admin.password = new_token
        admin.save(update_fields=['password'])  # 仅更新 password 字段，减少数据库写入

        # 5. 将用户 ID 和新令牌存入 Session
        request.session[self.SESSION_USER_ID_KEY] = admin.id
        request.session[self.SESSION_TOKEN_KEY] = new_token

        # 放行请求（已登录且刷新令牌）
        return None

    def process_response(self, request, response):
        """
        在响应返回前，将新生成的令牌写入 Cookie。
        仅针对受保护路径的响应，且仅当 Session 中存在新令牌时才写入。
        """
        if request.path.startswith(self.PROTECTED_PREFIX):
            new_token = request.session.get(self.SESSION_TOKEN_KEY)
            if new_token:
                response.set_cookie(
                    self.COOKIE_NAME,
                    new_token,
                    max_age=self.COOKIE_MAX_AGE,
                    path='/',
                    secure=request.is_secure(),  # 根据请求协议自动设置 Secure 标志
                    httponly=True,              # 防止 JavaScript 访问
                    samesite='Lax'              # 防御 CSRF
                )
        return response