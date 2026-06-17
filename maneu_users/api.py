from django.http import JsonResponse

from maneu_users import serivce
from maneu_users.forms.InsertForm import UserInsertForm
from maneu_users.forms.loginForm import LoginForm


def user_login(request):
    """登录接口"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['maneu_users'] = 'admin'
            res = {'code': 0, 'msg': '登录成功', 'data': {}}
        else:
            res = {'code': 2, 'msg': form.errors, 'data': {}}
    else:
        res = {'code': 1, 'msg': '请求错误', 'data': {}}
    return JsonResponse(res)


def user_list(request):
    if request.method == 'GET':
        find_user_all = serivce.find_user_all().values_list('user_id', 'nickname', 'status', 'level')
        res = {'code': 0, 'msg': 'succeed', 'data': list(find_user_all)}
    else:
        res = {'code': 1, 'msg': 'failed', 'data': []}
    return JsonResponse(res)


def user_insert(request):
    if request.method == 'POST':
        form = UserInsertForm(request.POST)
        if form.is_valid():
            add_user = serivce.add_user(form.clean())
            if type(add_user) == str:
                res = {'code': 3, 'msg': add_user, 'data': {}}
            else:
                res = {'code': 0, 'msg': '保存成功', 'data': {}}
        else:
            res = {'code': 2, 'msg': form.errors, 'data': {}}
    else:
        res = {'code': 1, 'msg': 'post', 'data': {}}
    return JsonResponse(res)


def user_update(request):
    if request.method == 'POST':
        form = UserInsertForm(request.POST)
        if form.is_valid():
            add_user = serivce.add_user(form.clean())
            if type(add_user) == str:
                res = {'code': 3, 'msg': add_user, 'data': {}}
            else:
                res = {'code': 0, 'msg': '保存成功', 'data': {}}
        else:
            res = {'code': 2, 'msg': form.errors, 'data': {}}
    else:
        res = {'code': 1, 'msg': 'post', 'data': {}}
    return JsonResponse(res)
