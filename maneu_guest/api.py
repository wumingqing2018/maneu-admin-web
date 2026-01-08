from django.forms import model_to_dict
from django.http import JsonResponse

from common.verify import is_uuid
from maneu_guest.service import *


def insert(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:
        try:
            guest_id = guest_insert(admin_id=admin_id,
                                    time=request.GET.get('time'),
                                    name=request.GET.get('name'),
                                    phone=request.GET.get('phone'),
                                    status=1,
                                    sex=request.GET.get('sex'),
                                    age=request.GET.get('age'),
                                    dfh=request.GET.get('DFH'),
                                    em=request.GET.get('EM'),
                                    ot=request.GET.get('OT'),
                                    remark=request.GET.get('remark')).id
            content = {'status': True, 'message': '', 'content': {'id': guest_id}}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)


def detail(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:

        guest_id = is_uuid(request.GET.get('guest_id'))
        if guest_id:
            try:
                data = guest_detail(admin_id=admin_id, guest_id=guest_id)
                guest_id = {'status': True, 'message': '', 'content': model_to_dict(data)}
            except Exception as e:
                guest_id = {'status': False, 'message': str(e), 'content': {}}
        else:
            guest_id = {'status': False, 'message': '请输入正确的参数', 'content': {}}

        content = {'status': True, 'message': '', 'content':{'guest_id': guest_id}}
    else:
        content = {'status': False, 'message': '账号异常', 'content':{'report_id': {}, 'guest_id': {}, 'order_id': {}}}
    return JsonResponse(content)


def delete(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:

        guest_id = is_uuid(request.GET.get('guest_id'))
        if guest_id:
            try:
                guest_id = guest_delete(admin_id=admin_id, guest_id=guest_id)[0]
            except Exception as e:
                guest_id = 0
        else:
            guest_id = 0

        content = {'status': True, 'message': '', 'content': {'guest_id': guest_id}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {'guest_id': {}}}
    return JsonResponse(content)


def update_time(request):
    guest_id = is_uuid(request.GET.get('guest_id'))
    admin_id = is_uuid(request.session.get('id'))

    if admin_id and guest_id:
        try:
            data = guest_update_time(guest_id=guest_id, admin_id=admin_id, time=request.GET.get('time'))
            content = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)


def update_data(request):
    guest_id = is_uuid(request.GET.get('guest_id'))
    admin_id = is_uuid(request.session.get('id'))

    if admin_id and guest_id:
        try:
            print(request.GET)
            data = guest_update_data(guest_id=guest_id,
                                     admin_id=admin_id,
                                     phone=request.GET.get('phone'),
                                     name=request.GET.get('name'),
                                     sex=request.GET.get('sex'),
                                     age=request.GET.get('age'),
                                     ot=request.GET.get('OT'),
                                     em=request.GET.get('EM'),
                                     dfh=request.GET.get('DFH'),
                                     remark=request.GET.get('guestRemark'),)
            content = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)


def search_time(request):
    admin_id = is_uuid(request.session.get('id'))

    if admin_id:
        try:
            data = guest_search_time(admin_id, request.GET.get('timeS'), request.GET.get('timeE'))
            content = {'status': True, 'message': admin_id, 'content': list(data.values('id','name','phone','time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)


def search_data(request):
    admin_id = is_uuid(request.session.get('id'))

    if admin_id:
        try:
            data = guest_search_data(admin_id, request.GET.get('value'))
            content = {'status': True, 'message': admin_id, 'content': list(data.values('id', 'name', 'phone', 'time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)
