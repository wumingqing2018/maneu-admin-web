from django.http import JsonResponse

from common import common
from common.jwt_util import *
from common.verify import is_call, is_code
from maneu import service


def sendsms(request):
    phone_number = is_call(request.GET.get('call'))

    if phone_number:
        code = common.get_random_code()
        if service.sendsms(call=phone_number, code=code) != 0:
            response = common.sendsms(call=phone_number, code=code)
            if response['Code'] == 'OK':
                content = {'status': True, 'message': 'OK', 'content': {}}
            else:
                content = {'status': False, 'message': response["Message"], 'content': {'code': code}}
        else:
            content = {'status': False, 'message': '请先注册账号', 'content': {}}
    else:
        content = {'status': False, 'message': '请输入正确账号', 'content': {}}

    return JsonResponse(content)


def access_token(request):
    call = is_call(request.GET.get('call'))
    code = is_code(request.GET.get('code'))
    if call and code:
        admin_user = service.admin_login(call=call, code=code)  # 需修改 service.admin_login 去掉 mark 依赖
        print(admin_user)
        if admin_user:
            a_token = generate_access_token(admin_user)
            print(a_token)
            r_token = generate_refresh_token(admin_user)
            print(r_token)
            content = {
                'status': True,
                'message': '100000',
                'content': {'access_token': a_token, 'refresh_token': r_token}
            }
        else:
            content = {'status': False, 'message': '验证码错误或手机号未注册'}
    else:
        content = {'status': False, 'message': '请填写手机号和验证码'}

    return JsonResponse(content)


def refresh_token(request):
    """刷新 access token（接收 refresh_token，返回新 access_token）"""
    token = request.GET.get('refresh_token')
    if not token:
        return JsonResponse({'status': False, 'message': '缺少 refresh_token'}, status=401)

    payload = verify_token(token, expected_type='refresh')
    if not payload:
        return JsonResponse({'status': False, 'message': 'refresh_token 无效或已过期'}, status=401)

    user = service.admin_find_id(payload['user_id'])
    if not payload:
        return JsonResponse({'status': False, 'message': '用户不存在'}, status=401)

    new_access_token = generate_access_token(user)
    # 如需滚动刷新，可同时生成新的 refresh_token 返回
    # new_refresh_token = generate_refresh_token(user)
    return JsonResponse({
        'status': True,
        'access_token': new_access_token,
        # 'refresh_token': new_refresh_token,   # 若启用滚动刷新取消注释
    })


def remove_token(request):
    """前端清除 token 后跳转登录页，这里只做重定向"""
    # 因为 JWT 无状态，服务端不需要任何操作
    content = {'status': True, 'message': 'OK', 'content': {}}
    return JsonResponse(content)
