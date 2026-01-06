import json

from django.forms import model_to_dict
from django.http import JsonResponse

from common.simple import order_simple, report_simple, guest_simple
from common.verify import is_uuid
from maneu_guest.service import guest_insert
from maneu_order.service import *
from maneu_report.service import report_insert


def search_time(request):
    admin_id = is_uuid(request.session.get('id'))

    if admin_id:
        try:
            data = order_search_time(admin_id=admin_id, timeS=request.GET.get('timeS'), timeE=request.GET.get('timeE')).values('id', 'report_id', 'guest_id', 'name', 'phone', 'time', 'remark')
            content = {'status': True, 'message': admin_id, 'content': list(data)}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)


def search_data(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:

        try:
            data = order_search_text(admin_id=admin_id, value=request.GET.get('value')).values('id', 'report_id', 'guest_id', 'name', 'phone', 'time', 'remark')
            content = {'status': True, 'message': admin_id, 'content': list(data)}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}

    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}
    return JsonResponse(content)


def update_time(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:

        order_id = is_uuid(request.GET.get('order_id'))
        if order_id:
            try:
                data = order_update(admin_id=admin_id, order_id=order_id, time=request.GET.get('time'))
                order_id = {'status': True, 'message': '', 'content': data}
            except Exception as e:
                order_id = {'status': False, 'message': str(e), 'content': {}}
        else:
            order_id = {'status': False, 'message': 'order_id 更新有误', 'content': {}}

        report_id = is_uuid(request.GET.get('report_id'))
        if report_id:
            try:
                data = order_update(admin_id=admin_id, report_id=report_id, time=request.GET.get('time'))
                report_id = {'status': True, 'message': '', 'content': data}
            except Exception as e:
                report_id = {'status': False, 'message': str(e), 'content': {}}
        else:
            report_id = {'status': False, 'message': 'order_id 更新有误', 'content': {}}

        guest_id = is_uuid(request.GET.get('guest_id'))
        if guest_id:
            try:
                data = order_update(admin_id=admin_id, guest_id=guest_id, time=request.GET.get('time'))
                guest_id = {'status': True, 'message': '', 'content': data}
            except Exception as e:
                guest_id = {'status': False, 'message': str(e), 'content': {}}
        else:
            guest_id = {'status': False, 'message': 'order_id 更新有误', 'content': {}}

        content = {'status': True, 'message': '', 'guest_id': guest_id, 'order_id': order_id, 'report_id': report_id}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'guest_id': {}, 'order_id': {}, 'report_id': {}}

    return JsonResponse(content)


def update_data(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:

        order_id = is_uuid(request.GET.get('order_id'))
        if order_id:
            try:
                data = order_update(admin_id=admin_id, order_id=order_id, time=request.GET.get('time'))
                order_id = {'status': True, 'message': '', 'content': data}
            except Exception as e:
                order_id = {'status': False, 'message': str(e), 'content': {}}
        else:
            order_id = {'status': False, 'message': 'order_id 更新有误', 'content': {}}

        report_id = is_uuid(request.GET.get('report_id'))
        if report_id:
            try:
                data = order_update(admin_id=admin_id, report_id=report_id, time=request.GET.get('time'))
                report_id = {'status': True, 'message': '', 'content': data}
            except Exception as e:
                report_id = {'status': False, 'message': str(e), 'content': {}}
        else:
            report_id = {'status': False, 'message': 'order_id 更新有误', 'content': {}}

        guest_id = is_uuid(request.GET.get('guest_id'))
        if guest_id:
            try:
                data = order_update(admin_id=admin_id, guest_id=guest_id, time=request.GET.get('time'))
                guest_id = {'status': True, 'message': '', 'content': data}
            except Exception as e:
                guest_id = {'status': False, 'message': str(e), 'content': {}}
        else:
            guest_id = {'status': False, 'message': 'order_id 更新有误', 'content': {}}

        content = {'status': True, 'message': '', 'guest_id': guest_id, 'order_id': order_id, 'report_id': report_id}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'guest_id': {}, 'order_id': {}, 'report_id': {}}

    return JsonResponse(content)


def insert(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:
        try:
            time = request.GET.get('time')
            name = request.GET.get('name')
            phone = request.GET.get('phone')

            content = guest_simple(request)
            guest_id = guest_insert(admin_id=admin_id, time=time, name=name, phone=phone, status=3,
                                    sex=request.GET.get('sex'), age=request.GET.get('age'), dfh=request.GET.get('DFH'),
                                    em=request.GET.get('EM'), ot=request.GET.get('OT'),
                                    remark=request.GET.get('remark')).id

            content = report_simple(request)
            report_id = report_insert(guest_id=guest_id, admin_id=admin_id, time=time, name=name, phone=phone, status=3,
                                      content=content).id

            content = order_simple(request.GET.get('content'))
            order = order_insert(admin_id=admin_id,
                                 guest_id=guest_id,
                                 report_id=report_id,
                                 time=time,
                                 name=name,
                                 phone=phone,
                                 status=3,
                                 content=content,
                                 remark=request.GET.get('remark'))

            content = {'status': True, 'message': '', 'content': {'id': order.id}}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)


def detail(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:

        order_id = is_uuid(request.GET.get('order_id'))
        if order_id:
            try:
                order = order_detail(order_id=order_id, admin_id=admin_id)
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
        else:
            order_id = {'status': False, 'message': '请输入正确的参数', 'content': {}}

        guest_id = is_uuid(request.GET.get('guest_id'))
        if guest_id:
            try:
                data = guest_detail(guest_id=guest_id, admin_id=admin_id)
                guest_id = {'status': True, 'message': '', 'content': model_to_dict(data)}
            except Exception as e:
                guest_id = {'status': False, 'message': str(e), 'content': {}}
        else:
            guest_id = {'status': False, 'message': '请输入正确的参数', 'content': {}}

        report_id = is_uuid(request.GET.get('report_id'))
        if report_id:
            try:
                data = report_detail(report_id=report_id, admin_id=admin_id)
                report_id = {'status': True, 'message': '', 'content': model_to_dict(data)}
            except Exception as e:
                report_id = {'status': False, 'message': str(e), 'content': {}}
        else:
            report_id = {'status': False, 'message': '请输入正确的参数', 'content': {}}

        content = {'status': True, 'message': '', 'report_id': report_id, 'guest_id': guest_id, 'order_id': order_id}
    else:
        content = {'status': False, 'message': '账号异常', 'report_id': '', 'guest_id': '', 'order_id': ''}
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

        order_id = is_uuid(request.GET.get('order_id'))
        if order_id:
            try:
                order_id = order_delete(admin_id=admin_id, order_id=order_id)[0]
            except Exception as e:
                order_id = 0
        else:
            order_id = 0

        report_id = is_uuid(request.GET.get('report_id'))
        if report_id:
            try:
                report_id = report_delete(admin_id=admin_id, report_id=report_id)[0]
            except Exception as e:
                report_id = 0
        else:
            report_id = 0

        content = {'status': True, 'message': '', 'guest_id': guest_id, 'order_id': order_id, 'report_id': report_id}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'guest_id': 0, 'order_id': '', 'report_id': ''}
    return JsonResponse(content)
