from django.forms import model_to_dict
from django.http import JsonResponse

from common.verify import is_uuid
from maneu_guest import service
from maneu.models import *


def search_time(request):
    admin_id = is_uuid(request.session.get('id'))

    if admin_id:
        try:
            data = service.guest_search_time(admin_id, request.GET.get('timeS'), request.GET.get('timeE')).values('id', 'name', 'phone', 'time', 'remark')
            print(data)
            content = {'status': True, 'message': admin_id, 'content': list(data)}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)


def search_text(request):
    admin_id = is_uuid(request.session.get('id'))

    if admin_id:
        try:
            data = service.guest_search_text(admin_id, request.GET.get('value')).values('id', 'name', 'phone', 'time',
                                                                                        'remark')
            print(data)
            content = {'status': True, 'message': admin_id, 'content': list(data)}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)

def insert(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:
        try:
            name = request.GET.get('name')
            time = request.GET.get('time')
            phone = request.GET.get('phone')
            status = 1

            guest_id = ManeuGuest.objects.create(admin_id=admin_id, time=time, name=name, phone=phone, status=status, sex=request.GET.get('sex'), age=request.GET.get('age'), dfh=request.GET.get('DFH'), em=request.GET.get('EM'), ot=request.GET.get('OT'), remark=request.GET.get('remark')).id
            content = {'status': True, 'message': '', 'content': {'id': guest_id}, 'mark': str(uuid4())}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}, 'mark': str(uuid4())}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)


def delete(request):
    admin_id = is_uuid(request.session.get('id'))
    guest_id = is_uuid(request.GET.get('order_id'))

    if admin_id and guest_id:
        try:
            data = service.ManeuGuest_delete(id=guest_id, admin_id=admin_id)
            content = {'status': True, 'message': '', 'content': list(data), 'mark': str(uuid4())}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}, 'mark': str(uuid4())}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)


def detail(request):
    guest_id = is_uuid(request.GET.get('id'))
    admin_id = is_uuid(request.session.get('id'))

    if admin_id and guest_id:
        try:
            data = service.ManeuGuest_detail(id=guest_id, admin_id=admin_id)
            content = {'status': True, 'message': '', 'content': model_to_dict(data), 'mark': str(uuid4())}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}, 'mark': str(uuid4())}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)


def update(request):
    guest_id = is_uuid(request.GET.get('guest_id'))
    admin_id = is_uuid(request.session.get('id'))

    if admin_id and guest_id:
        try:
            data = service.ManeuGuest_update(id=guest_id,
                                             admin_id=admin_id,
                                             phone=request.GET.get('call'),
                                             time=request.GET.get('time'),
                                             name=request.GET.get('name'),
                                             sex=request.GET.get('sex'),
                                             age=request.GET.get('age'),
                                             ot=request.GET.get('ot'),
                                             em=request.GET.get('em'),
                                             dfh=request.GET.get('dfh'),
                                             remark=request.GET.get('remark'))
            content = {'status': True, 'message': '', 'content': data, 'mark': str(uuid4())}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}, 'mark': str(uuid4())}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)
