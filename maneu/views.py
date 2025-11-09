from uuid import uuid4

from django.http import JsonResponse
from django.shortcuts import render

from common import common
from common import verify
from maneu import service


def index(request):
    return render(request, 'maneu/index.html')


def login(request):
    """
    登录模块
    获取session key并根据sessionkey 判断用户是否已经登录
    """
    return render(request, 'maneu/login.html')


def logout(request):
    code = verify.is_uuid(request.session.get('id'))
    print(code)

    if code:
        print(request.session.get('id'))
        request.session.clear()
        print(request.session.get('id'))
        data = service.admin_logout(code)
        if data:
            content = {'status': True, 'message': '', 'data': {}}
        else:
            content = {'status': False, 'message': '123', 'data': {}}
    else:
        content = {'status': False, 'message': '456', 'data': {}}

    return render(request, 'maneu/login.html')
