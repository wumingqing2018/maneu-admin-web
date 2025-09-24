from django.forms import model_to_dict
from django.http import JsonResponse

from common.simple import guest_simple
from common.verify import is_uuid
from maneu_guest import service


def search(request):
    admin_id = is_uuid(request.session.get('id'))
    value = request.GET.get('value')
    timeS = request.GET.get('timeS')
    timeE = request.GET.get('timeE')

    if admin_id and timeS and timeE:
        try:
            data = service.guest_search(admin_id, timeS, timeE, value).values('id', 'name', 'phone', 'time', 'remark')
            content = {'status': True, 'message': admin_id, 'data': list(data)}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'data': {}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'data': {}}

    return JsonResponse(content)


def insert(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:
        try:
            content = guest_simple(request)
            print(content)
            data = service.ManeuGuest_insert(admin_id=admin_id,
                                             time=content['time'],
                                             name=content['name'],
                                             phone=content['call'],
                                             sex=content['sex'],
                                             age=content['age'],
                                             dfh=content['dfh'],
                                             ot=content['ot'],
                                             em=content['em'],
                                             remark=content['remark'])

            content = {'status': True, 'message': '', 'data': {'id': data[0].id}}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'data': {}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'data': {}}

    return JsonResponse(content)


def delete(request):
    admin_id = is_uuid(request.session.get('id'))
    guest_id = is_uuid(request.GET.get('id'))

    if admin_id and guest_id:
        try:
            data = service.ManeuGuest_delete(id=guest_id, admin_id=admin_id)
            content = {'status': True, 'message': '', 'data': list(data)}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'data': {}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'data': {}}

    return JsonResponse(content)


def detail(request):
    guest_id = is_uuid(request.GET.get('id'))
    admin_id = is_uuid(request.session.get('id'))

    if admin_id and guest_id:
        try:
            data = service.ManeuGuest_detail(id=guest_id, admin_id=admin_id)
            content = {'status': True, 'message': '', 'data': model_to_dict(data)}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'data': {}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'data': {}}

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
            content = {'status': True, 'message': '', 'data': data}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'data': {}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'data': {}}

    return JsonResponse(content)
