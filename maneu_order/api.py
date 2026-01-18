import json
import uuid

from django.forms import model_to_dict
from django.http import JsonResponse

from common.simple import order_simple, report_simple, guest_simple
from common.verify import is_uuid
from maneu_guest.service import *
from maneu_order.service import *
from maneu_report.service import *


def insert(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:
        try:
            time = request.GET.get('time')
            name = request.GET.get('name')
            phone = request.GET.get('phone')
            index_id = uuid.uuid4()

            content = guest_simple(request)
            guest_id = guest_insert(index_id=index_id,
                                    admin_id=admin_id,
                                    time=time,
                                    name=name,
                                    phone=phone,
                                    status=3,
                                    sex=request.GET.get('sex'),
                                    age=request.GET.get('age'),
                                    dfh=request.GET.get('dfh'),
                                    em=request.GET.get('em'),
                                    ot=request.GET.get('ot'),
                                    remark=request.GET.get('guestRemark')).id

            content = report_simple(request)
            report_id = report_insert(index_id=index_id,
                                      guest_id=guest_id,
                                      admin_id=admin_id,
                                      time=time,
                                      name=name,
                                      phone=phone,
                                      status=3,
                                      content=content,
                                      remark=request.GET.get('reportRemark')).id

            content = order_simple(request.GET.get('content'))
            order_id = order_insert(index_id=index_id,
                                    admin_id=admin_id,
                                    time=time,
                                    name=name,
                                    phone=phone,
                                    status=3,
                                    content=content,
                                    remark=request.GET.get('orderRemark')).id

            content = {'status': True, 'message': '', 'content': {'id': order_id, 'guest_id': guest_id, 'report_id': report_id}}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}
    print(content)
    return JsonResponse(content)


def detail(request):
    admin_id = is_uuid(request.session.get('id'))
    index_id = is_uuid(request.GET.get('index_id'))
    if admin_id and index_id:
        try:
            data = report_detail(admin_id=admin_id, index_id=index_id)
            report_id = {'status': True, 'message': '', 'content': model_to_dict(data)}
        except Exception as e:
            report_id = {'status': False, 'message': str(e), 'content': {}}

        try:
            order = order_detail(admin_id=admin_id, index_id=index_id)
            content = {
                'time': order.time,
                'name': order.name,
                'phone': order.phone,
                'remark': order.remark,
                'content': json.loads(order.content),
            }
            order_id = {'status': True, 'message': '', 'content': content}
        except Exception as e:
            order_id = {'status': False, 'message': str(e), 'content': {}}

        try:
            data = guest_detail(admin_id=admin_id, index_id=index_id)
            guest_id = {'status': True, 'message': '', 'content': model_to_dict(data)}
        except Exception as e:
            guest_id = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '', 'content':{'report_id': report_id, 'guest_id': guest_id, 'order_id': order_id}}
    else:
        content = {'status': False, 'message': "admin_id"+ admin_id + "index_id"+ index_id, 'content':{'report_id': {}, 'guest_id': {}, 'order_id': {}}}
    return JsonResponse(content)


def delete(request):
    admin_id = is_uuid(request.session.get('id'))
    index_id = is_uuid(request.GET.get('index_id'))
    if admin_id and index_id:

        try:
            guest_id = guest_delete(admin_id=admin_id, index_id=index_id)[0]
        except Exception as e:
            guest_id = 0

        try:
            order_id = order_delete(admin_id=admin_id, index_id=index_id)[0]
        except Exception as e:
            order_id = 0

        try:
            report_id = report_delete(admin_id=admin_id, index_id=index_id)[0]
        except Exception as e:
            report_id = 0

        content = {'status': True, 'message': '', 'content': {'guest_id': guest_id, 'order_id': order_id, 'report_id': report_id}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {'guest_id': {}, 'order_id': {}, 'report_id': {}}}
    return JsonResponse(content)


def search_time(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:

        try:
            data = order_search_time(admin_id=admin_id, timeS=request.GET.get('timeS'), timeE=request.GET.get('timeE'))
            content = {'status': True, 'message': '', 'content': list(data.values('id', 'name', 'phone', 'time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}

    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}
    return JsonResponse(content)


def search_data(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:

        try:
            data = order_search_data(admin_id=admin_id, value=request.GET.get('value'))
            content = {'status': True, 'message': '', 'content': list(data.values('id', 'name', 'phone', 'time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}

    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}
    return JsonResponse(content)


def update_time(request):
    admin_id = is_uuid(request.session.get('id'))
    index_id = is_uuid(request.GET.get('index_id'))
    if admin_id:

        try:
            data = guest_update_time(admin_id=admin_id, index_id=index_id, time=request.GET.get('time'))
            guest_id = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            guest_id = {'status': False, 'message': str(e), 'content': {}}

        try:
            data = order_update_time(admin_id=admin_id, index_id=index_id, time=request.GET.get('time'))
            order_id = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            order_id = {'status': False, 'message': str(e), 'content': {}}

        try:
            data = report_update_time(admin_id=admin_id, index_id=index_id, time=request.GET.get('time'))
            report_id = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            report_id = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '', 'content': {'order_id': order_id, 'guest_id': guest_id, 'report_id': report_id}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {'guest_id': {}, 'order_id': {}, 'report_id': {}}}
    return JsonResponse(content)


def update(request):
    admin_id = is_uuid(request.session.get('id'))
    index_id = is_uuid(request.GET.get('index_id'))
    if admin_id and index_id:

        try:
            remark = request.GET.get('orderRemark')
            content = order_simple(request.GET.get('content'))
            data = order_update_data(admin_id=admin_id, index_id=index_id, content=content, remark=remark)
            content = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}

    else:
        content = {'status': False, 'message': '', 'content': {}}
    return JsonResponse(content)
