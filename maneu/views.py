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
    list = ManeuOrder.objects.all()
    for i in list:
        guest = ManeuGuest.objects.filter(id=i.guest_id).first()
        if guest:
            print(guest.id)
        else:
            guest = ManeuGuest.objects.create(name=i.name, phone=i.call, time=i.time, admin_id=i.admin_id, remark=i.remark)
            print(ManeuOrder.objects.filter(id=i.id).update(guest_id=guest.id))


def repair2(request):



    order = ManeuBuffer.objects.all()
    for order in order:
        content = ManeuGuest.objects.filter(admin_id=order.admin_id, phone=order.call).all().order_by('id')
        for i in list(content):
            print(i.admin_id,)



    Buffer = ManeuReport.objects.all()

    for i in Buffer:
        simple = {
            'PLAN': '远用解决方案',
            'PD': '',
            'OD_AL': '',
            'OD_AK': '',
            'OD_AX': 0.00,
            'OD_AD': '',
            'OD_ADD': 0.00,
            'OD_BC': '',
            'OD_CYL': 0.00,
            'OD_CCT': '',
            'OD_VA': '',
            'OD_SPH': 0.00,
            'OD_PR': '',
            'OD_FR': '',
            'OD_LT': '',
            'OD_VT': '',

            'OS_AL': '',
            'OS_AK': '',
            'OS_AX': 0.00,
            'OS_AD': '',
            'OS_ADD': 0.00,
            'OS_BC': '',
            'OS_CYL': 0.00,
            'OS_CCT': '',
            'OS_VA': '',
            'OS_SPH': 0.00,
            'OS_PR': '',
            'OS_FR': '',
            'OS_LT': '',
            'OS_VT': '',
        }

        content = i.content

        if content:
            content = json.loads(content)
            try:
                if content['OD']['AL']:
                    simple['OD_AL'] = content['OD']['AL']
                if content['OD']['AK']:
                    simple['OD_AK'] = content['OD']['AK']
                if content['OD']['AX']:
                    simple['OD_AX'] = content['OD']['AX']
                if content['OD']['AD']:
                    simple['OD_AD'] = content['OD']['AD']
                if content['OD']['ADD']:
                    simple['OD_ADD'] = content['OD']['ADD']
                if content['OD']['BC']:
                    simple['OD_BC'] = content['OD']['BC']
                if content['OD']['CYL']:
                    simple['OD_CYL'] = content['OD']['CYL']
                if content['OD']['CCT']:
                    simple['OD_CCT'] = content['OD']['CCT']
                if content['OD']['VA']:
                    simple['OD_VA'] = content['OD']['VA']
                if content['OD']['SPH']:
                    simple['OD_SPH'] = content['OD']['SPH']
                if content['OD']['PR']:
                    simple['OD_PR'] = content['OD']['PR']
                if content['OD']['FR']:
                    simple['OD_FR'] = content['OD']['FR']
                if content['OD']['LT']:
                    simple['OD_LT'] = content['OD']['LT']
                if content['OD']['VT']:
                    simple['OD_VT'] = content['OD']['VT']
                if content['OS']['AL']:
                    simple['OS_AL'] = content['OS']['AL']
                if content['OS']['AK']:
                    simple['OS_AK'] = content['OS']['AK']
                if content['OS']['AX']:
                    simple['OS_AX'] = content['OS']['AX']
                if content['OS']['AD']:
                    simple['OS_AD'] = content['OS']['AD']
                if content['OS']['ADD']:
                    simple['OS_ADD'] = content['OS']['ADD']
                if content['OS']['BC']:
                    simple['OS_BC'] = content['OS']['BC']
                if content['OS']['CYL']:
                    simple['OS_CYL'] = content['OS']['CYL']
                if content['OS']['CCT']:
                    simple['OS_CCT'] = content['OS']['CCT']
                if content['OS']['VA']:
                    simple['OS_VA'] = content['OS']['VA']
                if content['OS']['SPH']:
                    simple['OS_SPH'] = content['OS']['SPH']
                if content['OS']['PR']:
                    simple['OS_PR'] = content['OS']['PR']
                if content['OS']['FR']:
                    simple['OS_FR'] = content['OS']['FR']
                if content['OS']['LT']:
                    simple['OS_LT'] = content['OS']['LT']
                if content['OS']['VT']:
                    simple['OS_VT'] = content['OS']['VT']
                try:
                    simple['PLAN'] = content['PLAN']
                except Exception:
                    simple['PLAN'] = ''
                try:
                    simple['PD'] = content['PD']
                except Exception:
                    simple['PD'] = ''
                try:
                    print(ManeuBuffer.objects.create(id=i.id, admin_id=i.admin_id, guest_id=i.guest_id, remark=i.remark, time=i.time,
                                                     plan=simple['PLAN'],
                                                     pd=simple['PD'],
                                                     od_al=simple['OD_AL'],
                                                     od_ak=simple['OD_AK'],
                                                     od_ax=simple['OD_AX'],
                                                     od_ad=simple['OD_AD'],
                                                     od_add=simple['OD_ADD'],
                                                     od_bc=simple['OD_BC'],
                                                     od_cyl=simple['OD_CYL'],
                                                     od_cct=simple['OD_CCT'],
                                                     od_va=simple['OD_VA'],
                                                     od_sph=simple['OD_SPH'],
                                                     od_pr=simple['OD_PR'],
                                                     od_fr=simple['OD_FR'],
                                                     od_lt=simple['OD_LT'],
                                                     od_vt=simple['OD_VT'],
                                                     os_al=simple['OS_AL'],
                                                     os_ak=simple['OS_AK'],
                                                     os_ad=simple['OS_AD'],
                                                     os_ax=simple['OS_AX'],
                                                     os_add=simple['OS_ADD'],
                                                     os_bc=simple['OS_BC'],
                                                     os_cyl=simple['OS_CYL'],
                                                     os_cct=simple['OS_CCT'],
                                                     os_va=simple['OS_VA'],
                                                     os_sph=simple['OS_SPH'],
                                                     os_pr=simple['OS_PR'],
                                                     os_fr=simple['OS_FR'],
                                                     os_lt=simple['OS_LT'],
                                                     os_vt=simple['OS_VT'],))
                except Exception as e:
                    print(e)

            except Exception as e:
                for a in list(simple):
                    try:
                        simple[a] = content[a]
                    except:
                        pass
                try:
                    print(ManeuBuffer.objects.create(id=i.id, admin_id=i.admin_id, guest_id=i.guest_id, remark=i.remark, time=i.time,
                                                     plan=simple['PLAN'],
                                                     pd=simple['PD'],
                                                     od_al=simple['OD_AL'],
                                                     od_ak=simple['OD_AK'],
                                                     od_ax=simple['OD_AX'],
                                                     od_ad=simple['OD_AD'],
                                                     od_add=simple['OD_ADD'],
                                                     od_bc=simple['OD_BC'],
                                                     od_cyl=simple['OD_CYL'],
                                                     od_cct=simple['OD_CCT'],
                                                     od_va=simple['OD_VA'],
                                                     od_sph=simple['OD_SPH'],
                                                     od_pr=simple['OD_PR'],
                                                     od_fr=simple['OD_FR'],
                                                     od_lt=simple['OD_LT'],
                                                     od_vt=simple['OD_VT'],
                                                     os_al=simple['OS_AL'],
                                                     os_ak=simple['OS_AK'],
                                                     os_ad=simple['OS_AD'],
                                                     os_ax=simple['OS_AX'],
                                                     os_add=simple['OS_ADD'],
                                                     os_bc=simple['OS_BC'],
                                                     os_cyl=simple['OS_CYL'],
                                                     os_cct=simple['OS_CCT'],
                                                     os_va=simple['OS_VA'],
                                                     os_sph=simple['OS_SPH'],
                                                     os_pr=simple['OS_PR'],
                                                     os_fr=simple['OS_FR'],
                                                     os_lt=simple['OS_LT'],
                                                     os_vt=simple['OS_VT'],))
                except Exception as e:
                    print(e)

        else:
            try:
                print(ManeuBuffer.objects.create(id=i.id, admin_id=i.admin_id, guest_id=i.guest_id, remark=i.remark, time=i.time,
                                                 plan=simple['PLAN'],
                                                 pd=simple['PD'],
                                                 od_al=simple['OD_AL'],
                                                 od_ak=simple['OD_AK'],
                                                 od_ax=simple['OD_AX'],
                                                 od_ad=simple['OD_AD'],
                                                 od_add=simple['OD_ADD'],
                                                 od_bc=simple['OD_BC'],
                                                 od_cyl=simple['OD_CYL'],
                                                 od_cct=simple['OD_CCT'],
                                                 od_va=simple['OD_VA'],
                                                 od_sph=simple['OD_SPH'],
                                                 od_pr=simple['OD_PR'],
                                                 od_fr=simple['OD_FR'],
                                                 od_lt=simple['OD_LT'],
                                                 od_vt=simple['OD_VT'],
                                                 os_al=simple['OS_AL'],
                                                 os_ak=simple['OS_AK'],
                                                 os_ad=simple['OS_AD'],
                                                 os_ax=simple['OS_AX'],
                                                 os_add=simple['OS_ADD'],
                                                 os_bc=simple['OS_BC'],
                                                 os_cyl=simple['OS_CYL'],
                                                 os_cct=simple['OS_CCT'],
                                                 os_va=simple['OS_VA'],
                                                 os_sph=simple['OS_SPH'],
                                                 os_pr=simple['OS_PR'],
                                                 os_fr=simple['OS_FR'],
                                                 os_lt=simple['OS_LT'],
                                                 os_vt=simple['OS_VT'], ))
            except Exception as e:
                print(e)

    content = {'status': False, 'message': '请输入正确的手机号', 'data': ''}

    return JsonResponse(content)
