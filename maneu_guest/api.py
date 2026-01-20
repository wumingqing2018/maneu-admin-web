from django.forms import model_to_dict
from django.http import JsonResponse

from common.simple import guest_simple
from common.verify import is_uuid
from maneu_guest.service import *
from maneu_order.service import *
from maneu_report.service import *
import uuid

def insert(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:
        time = request.GET.get('time')
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        index_id = uuid.uuid4()

        try:
            content = guest_simple(request)
            guest_id = guest_insert(admin_id=admin_id, index_id=index_id, time=time, name=name, phone=phone, status=3, content=content, remark=request.GET.get('guestRemark')).id
            guest = {'status': True, 'message': guest_id, 'content': {}}
        except Exception as e:
            guest = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '', 'content': {'index_id': index_id, 'guest_id': guest}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {'index_id': "", 'guest_id': ""}}
    return JsonResponse(content)


def detail(request):
    admin_id = is_uuid(request.session.get('id'))
    index_id = is_uuid(request.GET.get('index_id'))
    if admin_id and index_id:

        try:
            data = guest_detail(admin_id=admin_id, index_id=index_id)
            guest_id = {'status': True, 'message': '', 'content': model_to_dict(data)}
        except Exception as e:
            guest_id = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '', 'content':{'guest_id': guest_id}}
    else:
        content = {'status': False, 'message': index_id, 'content':{'guest_id': {}}}
    return JsonResponse(content)


def delete(request):
    admin_id = is_uuid(request.session.get('id'))
    index_id = is_uuid(request.GET.get('index_id'))
    if admin_id and index_id:

        try:
            guest_delete(admin_id=admin_id, index_id=index_id)
            guest_id = {'status': True, 'message': "", 'content': {}}
        except Exception as e:
            guest_id = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '', 'content': {'guest_id': guest_id}}
    else:
        content = {'status': False, 'message': index_id, 'content':{'guest_id': {}}}
    return JsonResponse(content)


def update(request):
    admin_id = is_uuid(request.session.get('id'))
    index_id = is_uuid(request.GET.get('index_id'))
    if admin_id and index_id:

        try:
            data = guest_update_data(admin_id=admin_id,
                                     index_id=index_id,
                                     phone=request.GET.get('phone'),
                                     name=request.GET.get('name'),
                                     time=request.GET.get('time'),
                                     sex=request.GET.get('sex'),
                                     age=request.GET.get('age'),
                                     ot=request.GET.get('ot'),
                                     em=request.GET.get('em'),
                                     dfh=request.GET.get('dfh'),
                                     remark=request.GET.get('guestRemark'),)
            guest_id = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            guest_id = {'status': False, 'message': str(e), 'content': {}}


        try:
            data = order_update_time(admin_id=admin_id,
                                     index_id=index_id,
                                     time=request.GET.get('time'),
                                     name=request.GET.get('name'),
                                     phone=request.GET.get('phone'))
            order_id = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            order_id = {'status': False, 'message': str(e), 'content': {}}


        try:
            data = report_update_time(admin_id=admin_id,
                                      index_id=index_id,
                                      time=request.GET.get('time'),
                                      name=request.GET.get('name'),
                                      phone=request.GET.get('phone'))
            report_id = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            report_id = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '', 'content': {'order_id': order_id, 'guest_id': guest_id, 'report_id': report_id}}
    else:
        content = {'status': True, 'message': '', 'content': {'order_id': {}, 'guest_id': {}, 'report_id': {}}}
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
