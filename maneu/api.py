from common import common
from common.forms.sendSMSForm import SendSMSForm
from common.forms.userLoginForm import UserLoginForm

from common.jwt_util import *
from maneu import service

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.cache import cache


@csrf_exempt  # 因为使用 JWT，无需 CSRF
@require_http_methods(["POST"])  # 只允许 POST
def sendsms(request):
    form = SendSMSForm(request.POST)
    if form.is_valid():
        call = form.cleaned_data['call']
        code = form.cleaned_data['code']

        # 存储验证码，有效期5分钟（与表单频率限制时间段不同，可取交集）
        cache.set(call, code, timeout=300)

        # 发送短信...（调用阿里云接口）
        common_sendsms = common.sendsms(call, code)
        if common_sendsms:
            return JsonResponse({'status': True, 'message': '验证码已发送', 'content': {}})
        else:
            return JsonResponse({'status': False, 'message': msg, 'content': {}})
    else:
        return JsonResponse({'status': False, 'message': form.errors.as_text(), 'content': {}})


@csrf_exempt  # 因为使用 JWT，无需 CSRF
@require_http_methods(["POST"])  # 只允许 POST
def access_token(request):
    form = UserLoginForm(request.POST)

    if form.is_valid():
        call = form.cleaned_data['call']
        user = service.admin_find_username(code=call)
        a_token = generate_access_token(user)
        r_token = generate_refresh_token(user)
        content = {'status': True, 'message': '登录成功', 'content': {'access_token': a_token,'refresh_token': r_token}}
    else:
        content = {'status': False, 'message': form.errors.as_text(), 'content': {}}

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
