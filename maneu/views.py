import uuid

from django.http import JsonResponse
from django.shortcuts import render

from common import common
from common import verify
from maneu import service
from maneu.models import *
import json


def index(request):
    """
    首页
    """
    return render(request, 'maneu/index.html')


def login(request):
    """
    登录模块
    获取session key并根据sessionkey 判断用户是否已经登录
    """
    return render(request, 'maneu/login.html')


def login_api(request):
    call = verify.is_call(request.GET.get('call'))
    code = verify.is_code(request.GET.get('code'))
    if call and code:
        adminUser = service.admin_login(call, code)
        if adminUser:
            mark = str(uuid.uuid4())
            request.session['ip'] = common.getip(request)
            request.session['id'] = adminUser.id
            request.session['nickname'] = adminUser.nickname
            request.session['mark'] = mark
            content = {'status': True, 'message': '100000', 'content': {'password': adminUser.password}, 'mark': mark, }
        else:
            content = {'status': False, 'message': '100002', 'content': {}}
    else:
        content = {'status': False, 'message': '100001', 'content': {}}

    return JsonResponse(content)


def login_api2(request):
    call = verify.is_call(request.GET.get('call'))
    code = verify.is_code(request.GET.get('code'))
    if call and code:
        adminUser = service.admin_login(call, code)
        print(adminUser)
        if adminUser:
            code = uuid.uuid4()
            request.session['ip'] = common.getip(request)
            request.session['id'] = adminUser.id
            request.session['nickname'] = adminUser.nickname
            request.session['code'] = code
            content = {'status': True, 'message': '', 'data': {'code': code}}
        else:
            content = {'status': False, 'message': '100002', 'data': {'code': code}}
    else:
        content = {'status': False, 'message': '100001', 'data': {}}

    return JsonResponse(content)


def logout(request):
    code = verify.is_code(request.session.get('id'))

    if code:
        request.session['ip'] = None
        request.session['id'] = None
        request.session['nickname'] = None
        data = service.admin_logout(code)
        if data:
            content = {'status': True, 'message': '', 'data': {}}
        else:
            content = {'status': False, 'message': '123', 'data': {}}
    else:
        content = {'status': False, 'message': '456', 'data': {}}

    return render(request, 'maneu/login.html')


def sendsms(request):
    phone_number = verify.is_call(request.GET.get('call'))
    if phone_number:
        code = str(common.get_random_code())
        data = service.sendsms(call=phone_number, code=code)
        if data:
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


def repair(request):
    Buffer = ManeuBuffer.objects.all()

    for i in Buffer:
        content = ManeuRefraction.objects.filter(id=i.id).first()
        if content:
            content = content.content
            if content[0:9] == '{"OD_VA":':
                content = json.loads(content)
                if content['OD_SPH']:
                    OD_SPH = content['OD_SPH']
                else:
                    OD_SPH = 0.00
                if content['OS_SPH']:
                    OS_SPH = content['OS_SPH']
                else:
                    OS_SPH = 0.00

                if content['OD_CYL']:
                    OD_CYL = content['OD_CYL']
                else:
                    OD_CYL = 0.00
                if content['OS_CYL']:
                    OS_CYL = content['OS_CYL']
                else:
                    OS_CYL = 0.00

                if content['OD_VA']:
                    OD_VA = content['OD_VA']
                else:
                    OD_VA = 5.00
                if content['OS_VA']:
                    OS_VA = content['OS_VA']
                else:
                    OS_VA = 5.00

                if content['OD_AX']:
                    OD_AX = content['OD_AX']
                else:
                    OD_AX = 23.5
                if content['OS_AX']:
                    OS_AX = content['OS_AX']
                else:
                    OS_AX = 23.5

                try:
                    if content['OD_ADD']:
                        OD_ADD = content['OD_ADD']
                    else:
                        OD_ADD = 0.00
                    if content['OS_ADD']:
                        OS_ADD = content['OS_ADD']
                    else:
                        OS_ADD = 0.00
                except Exception:
                    OS_ADD = 0.00
                    OD_ADD = 0.00
                try:
                    plan = content['function']
                except Exception:
                    plan = ''
                try:
                    pd = content['PD']
                except Exception:
                    pd = ''

                print(ManeuBuffer.objects.filter(id=i.id).update(plan=plan, pd=pd, od_va=OD_VA, od_sph=OD_SPH, od_cyl=OD_CYL, od_add=OD_ADD, od_ax=OD_AX, os_va=OS_VA, os_sph=OS_SPH, os_cyl=OS_CYL, os_add=OS_ADD, os_ax=OS_AX,))
            elif content[0:9] == '{"OS_VA":':
                content = json.loads(content)
                if content['OD_SPH']:
                    OD_SPH = content['OD_SPH']
                else:
                    OD_SPH = 0.00
                if content['OS_SPH']:
                    OS_SPH = content['OS_SPH']
                else:
                    OS_SPH = 0.00

                if content['OD_CYL']:
                    OD_CYL = content['OD_CYL']
                else:
                    OD_CYL = 0.00
                if content['OS_CYL']:
                    OS_CYL = content['OS_CYL']
                else:
                    OS_CYL = 0.00

                if content['OD_VA']:
                    OD_VA = content['OD_VA']
                else:
                    OD_VA = 5.00
                if content['OS_VA']:
                    OS_VA = content['OS_VA']
                else:
                    OS_VA = 5.00

                if content['OD_AX']:
                    OD_AX = content['OD_AX']
                else:
                    OD_AX = 23.5
                if content['OS_AX']:
                    OS_AX = content['OS_AX']
                else:
                    OS_AX = 23.5

                try:
                    if content['OD_ADD']:
                        OD_ADD = content['OD_ADD']
                    else:
                        OD_ADD = 0.00
                    if content['OS_ADD']:
                        OS_ADD = content['OS_ADD']
                    else:
                        OS_ADD = 0.00
                except Exception:
                    OS_ADD = 0.00
                    OD_ADD = 0.00
                try:
                    plan = content['function']
                except Exception:
                    plan = ''
                try:
                    pd = content['PD']
                except Exception:
                    pd = ''

                print(ManeuBuffer.objects.filter(id=i.id).update(plan=plan, pd=pd, od_va=OD_VA, od_sph=OD_SPH, od_cyl=OD_CYL, od_add=OD_ADD, od_ax=OD_AX, os_va=OS_VA, os_sph=OS_SPH, os_cyl=OS_CYL, os_add=OS_ADD, os_ax=OS_AX,))
            elif content[0:9] == '{"OD_SPH"':
                content = json.loads(content)
                if content['OD_SPH']:
                    OD_SPH = content['OD_SPH']
                else:
                    OD_SPH = 0.00
                if content['OS_SPH']:
                    OS_SPH = content['OS_SPH']
                else:
                    OS_SPH = 0.00

                if content['OD_CYL']:
                    OD_CYL = content['OD_CYL']
                else:
                    OD_CYL = 0.00
                if content['OS_CYL']:
                    OS_CYL = content['OS_CYL']
                else:
                    OS_CYL = 0.00

                if content['OD_AX']:
                    OD_AX = content['OD_AX']
                else:
                    OD_AX = 23.5
                if content['OS_AX']:
                    OS_AX = content['OS_AX']
                else:
                    OS_AX = 23.5

                try:
                    OD_ADD = content['OD_ADD']
                    OS_ADD = content['OS_ADD']

                except Exception:
                    OD_ADD = 0.00
                    OS_ADD = 0.00

                print(ManeuBuffer.objects.filter(id=i.id).update(plan=content['function'], pd=content['PD'], od_va='', od_sph=OD_SPH, od_cyl=OD_CYL, od_add=OD_ADD, od_ax=OD_AX, os_va='', os_sph=OS_SPH, os_cyl=OS_CYL, os_add=OS_ADD, os_ax=OS_AX,))
            elif content[0:9] == '{"PLAN": ':
                content = json.loads(content)
                if content['OD']['SPH']:
                    OD_SPH = content['OD']['SPH']
                else:
                    OD_SPH = 0.00
                if content['OS']['SPH']:
                    OS_SPH = content['OS']['SPH']
                else:
                    OS_SPH = 0.00

                if content['OD']['CYL']:
                    OD_CYL = content['OD']['CYL']
                else:
                    OD_CYL = 0.00
                if content['OS']['CYL']:
                    OS_CYL = content['OS']['CYL']
                else:
                    OS_CYL = 0.00

                if content['OD']['AX']:
                    OD_AX = content['OD']['AX']
                else:
                    OD_AX = 23.5
                if content['OS']['AX']:
                    OS_AX = content['OS']['AX']
                else:
                    OS_AX = 23.5

                try:
                    if content['OD']['ADD']:
                        OD_ADD = content['OD']['ADD']
                    else:
                        OD_ADD = 0.00
                    if content['OS']['ADD']:
                        OS_ADD = content['OS']['ADD']
                    else:
                        OS_ADD = 0.00
                except Exception:
                    OD_ADD = 0.00
                    OS_ADD = 0.00

                try:
                    plan = content['PLAN']
                except Exception:
                    plan = ''
                try:
                    pd = content['PD']
                except Exception:
                    pd = ''

                print(ManeuBuffer.objects.filter(id=i.id).update(plan=plan, pd=pd, od_va='', od_sph=OD_SPH, od_cyl=OD_CYL, od_add=OD_ADD, od_ax=OD_AX, os_va='', os_sph=OS_SPH, os_cyl=OS_CYL, os_add=OS_ADD, os_ax=OS_AX,))
            elif content[0:7] == '{"PD": ':
                content = json.loads(content)
                if content['OD']['SPH']:
                    OD_SPH = content['OD']['SPH']
                else:
                    OD_SPH = 0.00
                if content['OS']['SPH']:
                    OS_SPH = content['OS']['SPH']
                else:
                    OS_SPH = 0.00

                if content['OD']['CYL']:
                    OD_CYL = content['OD']['CYL']
                else:
                    OD_CYL = 0.00
                if content['OS']['CYL']:
                    OS_CYL = content['OS']['CYL']
                else:
                    OS_CYL = 0.00

                if content['OD']['AX']:
                    OD_AX = content['OD']['AX']
                else:
                    OD_AX = 23.5
                if content['OS']['AX']:
                    OS_AX = content['OS']['AX']
                else:
                    OS_AX = 23.5

                try:
                    if content['OD']['ADD']:
                        OD_ADD = content['OD']['ADD']
                    else:
                        OD_ADD = 0.00
                    if content['OS']['ADD']:
                        OS_ADD = content['OS']['ADD']
                    else:
                        OS_ADD = 0.00
                except Exception:
                    OD_ADD = 0.00
                    OS_ADD = 0.00

                try:
                    plan = content['PLAN']
                except Exception:
                    plan = ''
                try:
                    pd = content['PD']
                except Exception:
                    pd = ''

                print(
                    ManeuBuffer.objects.filter(id=i.id).update(plan=plan, pd=pd, od_va='', od_sph=OD_SPH, od_cyl=OD_CYL,
                                                               od_add=OD_ADD, od_ax=OD_AX, os_va='', os_sph=OS_SPH,
                                                               os_cyl=OS_CYL, os_add=OS_ADD, os_ax=OS_AX, ))
            elif content[0:9] == '{"time":"':
                content = json.loads(content)
                if content['OD_SPH']:
                    OD_SPH = content['OD_SPH']
                else:
                    OD_SPH = 0.00
                if content['OS_SPH']:
                    OS_SPH = content['OS_SPH']
                else:
                    OS_SPH = 0.00

                if content['OD_CYL']:
                    OD_CYL = content['OD_CYL']
                else:
                    OD_CYL = 0.00
                if content['OS_CYL']:
                    OS_CYL = content['OS_CYL']
                else:
                    OS_CYL = 0.00

                try:
                    if content['OD_VA']:
                        OD_VA = content['OD_VA']
                    else:
                        OD_VA = 5.00
                    if content['OS_VA']:
                        OS_VA = content['OS_VA']
                    else:
                        OS_VA = 5.00
                except:
                    OD_VA = ''
                    OS_VA = ''

                if content['OD_AX']:
                    OD_AX = content['OD_AX']
                else:
                    OD_AX = 23.5
                if content['OS_AX']:
                    OS_AX = content['OS_AX']
                else:
                    OS_AX = 23.5
                try:
                    if content['OD_ADD']:
                        OD_ADD = content['OD_ADD']
                    else:
                        OD_ADD = 0.00
                    if content['OS_ADD']:
                        OS_ADD = content['OS_ADD']
                    else:
                        OS_ADD = 0.00
                except Exception:
                    OD_ADD = 0.00
                    OS_ADD = 0.00
                try:
                    plan = content['function']
                except Exception:
                    plan = ''
                try:
                    pd = content['PD']
                except Exception:
                    pd = ''

                print(ManeuBuffer.objects.filter(id=i.id).update(plan=plan, pd=pd, od_va=OD_VA, od_sph=OD_SPH, od_cyl=OD_CYL, od_add=OD_ADD, od_ax=OD_AX, os_va=OS_VA, os_sph=OS_SPH, os_cyl=OS_CYL, os_add=OS_ADD, os_ax=OS_AX,))
            else:
                print(content[0:9])

    content = {'status': False, 'message': '请输入正确的手机号',
               'data': ''}

    return JsonResponse(content)
