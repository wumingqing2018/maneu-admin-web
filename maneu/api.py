from common import common
from common.forms.sendSMSForm import SendSMSForm
from common.forms.userLoginForm import UserLoginForm

from common.jwt_util import *
from maneu import service

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt  # 因为使用 JWT，无需 CSRF
@require_http_methods(["POST"])  # 只允许 POST
def sendsms(request):
    form = SendSMSForm(request.POST)
    if form.is_valid():
        call = form.cleaned_data['call']
        code = form.cleaned_data['code']  # 由表单 clean 生成的验证码

        # 调用短信发送服务
        response = common.sendsms(call=call, code=code)
        if response.get('Code') == 'OK':
            content = {'status': True,'message': '验证码已发送', 'content': {}}
        else:
            content = {'status': False, 'message': response["Message"], 'content': {}}
    else:
        content = {'status': False, 'message': form.errors.as_text(), 'content': {}}
    return JsonResponse(content)



@csrf_exempt  # 因为使用 JWT，无需 CSRF
@require_http_methods(["POST"])  # 只允许 POST
def access_token(request):
    form = UserLoginForm(request.POST)

    if form.is_valid():
        # 从表单获取已验证的用户对象（假设你在 form.clean() 中设置了 'user'）
        user = form.cleaned_data['user']
        a_token = generate_access_token(user)
        r_token = generate_refresh_token(user)
        content = {'status': True, 'message': '登录成功', 'content': {'access_token': a_token,'refresh_token': r_token}}
    else:
        content = {'status': True, 'message': form.errors.as_text(), 'content': {}}

    return JsonResponse(content)



@csrf_exempt  # 因为使用 JWT，无需 CSRF
@require_http_methods(["POST"])  # 只允许 POST
def refresh_token(request):
    """刷新 access token（接收 refresh_token，返回新 access_token）"""
    token = request.POST.get('refresh_token')
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
    content = {'status': True, 'message': 'OK', 'content': {}}
    return JsonResponse(content)
