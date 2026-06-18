import uuid

from django.forms import model_to_dict
from django.http import JsonResponse

from common.simple import extract_guest_simple_params
from common.verify import is_uuid
from maneu_guest.service import *
from common.jwt_util import _get_admin_id


def insert(request):
    admin_id = _get_admin_id(request)
    if admin_id:
        time = request.POST.get('time')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        index_id = uuid.uuid4()

        try:
            content = extract_guest_simple_params(request)
            guest_id = guest_insert(admin_id=admin_id, index_id=index_id, time=time, name=name, phone=phone, status=3,
                                    content=content, remark=request.POST.get('guestRemark')).id
            guest = {'status': True, 'message': guest_id, 'content': {}}
        except Exception as e:
            guest = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '', 'content': {'index_id': index_id, 'guest_id': guest}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {'index_id': "", 'guest_id': ""}}
    return JsonResponse(content)


def detail(request):
    admin_id = _get_admin_id(request)
    index_id = is_uuid(request.POST.get('index_id'))
    if admin_id and index_id:

        try:
            data = guest_detail(admin_id=admin_id, index_id=index_id)
            guest_id = {'status': True, 'message': '', 'content': model_to_dict(data)}
        except Exception as e:
            guest_id = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '', 'content': {'guest_id': guest_id}}
    else:
        content = {'status': False, 'message': index_id, 'content': {'guest_id': {}}}
    return JsonResponse(content)


def delete(request):
    admin_id = _get_admin_id(request)
    index_id = is_uuid(request.POST.get('index_id'))
    if admin_id and index_id:

        try:
            guest_delete(admin_id=admin_id, index_id=index_id)
            guest_id = {'status': True, 'message': "", 'content': {}}
        except Exception as e:
            guest_id = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '', 'content': {'guest_id': guest_id}}
    else:
        content = {'status': False, 'message': index_id, 'content': {'guest_id': {}}}
    return JsonResponse(content)


def update(request):
    admin_id = _get_admin_id(request)
    index_id = is_uuid(request.POST.get('index_id'))
    if admin_id and index_id:

        try:
            data = guest_update(admin_id=admin_id,
                                index_id=index_id,
                                phone=request.POST.get('phone'),
                                name=request.POST.get('name'),
                                time=request.POST.get('time'),
                                sex=request.POST.get('sex'),
                                age=request.POST.get('age'),
                                ot=request.POST.get('ot'),
                                em=request.POST.get('em'),
                                dfh=request.POST.get('dfh'),
                                remark=request.POST.get('guestRemark'))
            guest = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            guest = {'status': False, 'message': str(e), 'content': {}}

        try:
            data = order_update(admin_id=admin_id,
                                index_id=index_id,
                                time=request.POST.get('time'),
                                name=request.POST.get('name'),
                                phone=request.POST.get('phone'),
                                remark=request.POST.get('guestRemark'))

            order = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            order = {'status': False, 'message': str(e), 'content': {}}

        try:
            data = store_update(admin_id=admin_id,
                                index_id=index_id,
                                time=request.POST.get('time'),
                                name=request.POST.get('name'),
                                phone=request.POST.get('phone'),
                                remark=request.POST.get('guestRemark'))

            store = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            store = {'status': False, 'message': str(e), 'content': {}}

        try:
            data = report_update(admin_id=admin_id,
                                 index_id=index_id,
                                 time=request.POST.get('time'),
                                 name=request.POST.get('name'),
                                 phone=request.POST.get('phone'),
                                 remark=request.POST.get('guestRemark'))

            report = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            report = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '',
                   'content': {'order': order, 'guest': guest, 'store': store, 'report': report}}
    else:
        content = {'status': True, 'message': '', 'content': {'order': {}, 'guest': {}, 'store': {}, 'report': {}}}
    return JsonResponse(content)


def search_time(request):
    admin_id = _get_admin_id(request)

    if admin_id:
        try:
            data = guest_search_time(admin_id, request.POST.get('timeS'), request.POST.get('timeE'))
            content = {'status': True, 'message': admin_id,
                       'content': list(data.values('id', 'name', 'phone', 'time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)


def search_data(request):
    admin_id = _get_admin_id(request)

    if admin_id:
        try:
            data = guest_search_data(admin_id, request.POST.get('value'))
            content = {'status': True, 'message': admin_id,
                       'content': list(data.values('id', 'name', 'phone', 'time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)
