import json
from uuid import uuid4

from django.http import JsonResponse

from common.simple import order_simple
from common.verify import is_uuid
from maneu_order import service


def search_time(request):
    admin_id = is_uuid(request.session.get('id'))

    if admin_id:
        try:
            data = service.order_search_time(admin_id, request.GET.get('timeS'), request.GET.get('timeE')).values('id', 'name', 'phone', 'time', 'remark')
            print(data)
            content = {'status': True, 'message': admin_id, 'content': list(data), 'mark': uuid4()}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}, 'mark': uuid4()}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)


def search_text(request):
    admin_id = is_uuid(request.session.get('id'))

    if admin_id:
        try:
            data = service.order_search_text(admin_id, request.GET.get('value')).values('id', 'name', 'phone', 'time',
                                                                                        'remark')
            print(data)
            content = {'status': True, 'message': admin_id, 'content': list(data), 'mark': uuid4()}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}, 'mark': uuid4()}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)


def insert(request):
    admin_id = is_uuid(request.session.get('id'))
    guest_id = is_uuid(request.GET.get('guest_id'))
    report_id = is_uuid(request.GET.get('report_id'))

    if admin_id and guest_id and report_id:
        try:
            content = order_simple(request.GET.get('content'))
            order = service.order_insert(admin_id=admin_id,
                                         guest_id=guest_id,
                                         report_id=report_id,
                                         time=request.GET.get('time'),
                                         name=request.GET.get('name'),
                                         call=request.GET.get('call'),
                                         content=content,
                                         remark=request.GET.get('remark'))
            content = {'status': True, 'message': '', 'content': {'id': order.id}, 'mark': uuid4()}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}, 'mark': uuid4()}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)


def update(request):
    admin_id = is_uuid(request.session.get('id'))
    order_id = is_uuid(request.GET.get('order_id'))

    if admin_id and order_id:
        try:
            content = order_simple(request.GET.get('content'))
            order = service.order_update(admin_id=admin_id,
                                         order_id=order_id,
                                         time=request.GET.get('time'),
                                         name=request.GET.get('name'),
                                         call=request.GET.get('call'),
                                         content=content,
                                         remark=request.GET.get('remark'))
            content = {'status': True, 'message': '', 'content': order, 'mark': uuid4()}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}, 'mark': uuid4()}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)


def detail(request):
    order_id = is_uuid(request.GET.get('id'))
    admin_id = is_uuid(request.session.get('id'))

    if admin_id and order_id:
        try:
            order = service.order_detail(order_id=order_id, admin_id=admin_id)
            content = {
                'content': json.loads(order.content),
                'guest_id': order.guest_id,
                'report_id': order.report_id,
                'name': order.name,
                'phone': order.phone,
                'remark': order.remark,
                'time': order.time
            }
            content = {'status': True, 'message': '', 'content': content, 'mark': uuid4()}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}, 'mark': uuid4()}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)


def delete(request):
    order_id = is_uuid(request.GET.get('id'))
    admin_id = is_uuid(request.session.get('id'))

    if admin_id and order_id:
        try:
            data = service.order_delete(order_id=order_id, admin_id=admin_id)
            content = {'status': True, 'message': '', 'content': data, 'mark': uuid4()}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}, 'mark': uuid4()}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)
