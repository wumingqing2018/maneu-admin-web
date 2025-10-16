from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from common.verify import is_uuid


class UserMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response
        print("--用户登录校验中间件启动--")

    def process_request(self, request):
        """
        产生request对象之后---url匹配之前调用
        判断用户是否登录
        白名单内app, 不需要登录
        用户没有登录, 跳转到登录页
        用户已经登录, 允许通过
        """
        print(request)
        request_url = request.path  # method:string, demo:/login/,
        session_ip = request.session.get('ip')
        session_code = is_uuid(request.GET.get('code'))
        #   判断是否需要校验字段
        if request_url.startswith('/maneu'):
            if request.session['ip'] == session_ip and request.session['code'] == session_code:
                return None
            else:
                request.session.clear()
                return redirect('login')
        return None
