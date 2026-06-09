from uuid import uuid4

from django.http import JsonResponse

from common import common
from common.verify import is_call, is_code, is_uuid
from maneu import service
from maneu.views import login


def sendsms(request):
    phone_number = is_call(request.GET.get('call'))

    if phone_number:
        code = common.get_random_code()
        if service.sendsms(call=phone_number, code=code) != 0:
            response = common.sendsms(call=phone_number, code=code)
            if response['Code'] == 'OK':
                content = {'status': True, 'message': 'OK', 'data': {}}
            else:
                content = {'status': False, 'message': response["Message"], 'data': {'code': code}}
        else:
            content = {'status': False, 'message': '请输入正确的手机号', 'data': {}}
    else:
        content = {'status': False, 'message': '请输入正确的手机号', 'data': {}}

    return JsonResponse(content)


def login_api(request):
    call = is_call(request.GET.get('call'))
    code = is_code(request.GET.get('code'))
    mark = str(uuid4())
    if call and code:
        adminUser = service.admin_login(call=call, code=code, mark=mark)
        if adminUser != 0:
            request.session['ip'] = common.getip(request)
            request.session['mark'] = mark
            content = {'status': True, 'message': '100000', 'content': {}}
        else:
            content = {'status': False, 'message': '100002', 'content': {}}
    else:
        content = {'status': False, 'message': '100001', 'content': {}}
    print(content)
    response = JsonResponse(content)
    response.set_cookie(key='mark',  # cookie 名称
                        value=mark,  # cookie 值
                        max_age=3600,  # 过期时间（秒）
                        path='/',  # 生效路径
                        secure=True,  # 仅通过 HTTPS 传输
                        httponly=True,  # 防止 JavaScript 访问
                        samesite='Lax'  # 防止 CSRF 攻击
                        )
    return response


def logout(request):
    code = is_uuid(request.session.get('id'))

    if code:

        data = service.admin_logout(code)
        if data:
            content = {'status': True, 'message': '', 'data': {}}
        else:
            content = {'status': False, 'message': '123', 'data': {}}
    else:
        content = {'status': False, 'message': '456', 'data': {}}

    return login(request)
