from django.forms import model_to_dict
from django.http import JsonResponse

from common.verify import is_uuid
from maneu_guest.service import *
from maneu_order.service import *
from maneu_report.service import *


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
                                    dfh=request.GET.get('dfh'),
                                    em=request.GET.get('em'),
                                    ot=request.GET.get('ot'),
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


def update(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:

        guest_id = is_uuid(request.GET.get('guest_id'))
        if guest_id:
            try:
                data = guest_update_data(guest_id=guest_id,
                                         admin_id=admin_id,
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
        else:
            guest_id = {'status': False, 'message': '参数错误请确认', 'content': {}}

        order_id = is_uuid(request.GET.get('order_id'))
        if order_id:
            try:
                data = order_update_time(admin_id=admin_id, order_id=order_id, time=request.GET.get('time'), name=request.GET.get('name'), phone=request.GET.get('phone'))
                order_id = {'status': True, 'message': '', 'content': data}
            except Exception as e:
                order_id = {'status': False, 'message': str(e), 'content': {}}
        else:
            order_id = {'status': False, 'message': 'order_id 更新有误', 'content': {}}

        report_id = is_uuid(request.GET.get('report_id'))
        if report_id:
            try:
                data = report_update_time(admin_id=admin_id, report_id=report_id, time=request.GET.get('time'), name=request.GET.get('name'), phone=request.GET.get('phone'))
                report_id = {'status': True, 'message': '', 'content': data}
            except Exception as e:
                report_id = {'status': False, 'message': str(e), 'content': {}}
        else:
            report_id = {'status': False, 'message': 'order_id 更新有误', 'content': {}}

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
