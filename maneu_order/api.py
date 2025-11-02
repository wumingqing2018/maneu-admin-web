import json
from uuid import uuid4

from django.http import JsonResponse

from common.simple import order_simple, report_simple
from common.verify import is_uuid
from maneu.models import ManeuGuest
from maneu_order import service
from maneu_report.service import report_insert


def search_time(request):
    admin_id = is_uuid(request.session.get('id'))

    if admin_id:
        try:
            data = service.order_search_time(admin_id, request.GET.get('timeS'), request.GET.get('timeE')).values('id',
                                                                                                                  'name',
                                                                                                                  'phone',
                                                                                                                  'time',
                                                                                                                  'remark')
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
    phone = request.GET.get('phone')
    time = request.GET.get('time')
    print(admin_id, phone, time)
    if admin_id and phone:
        try:
            guest = ManeuGuest.objects.filter(admin_id=admin_id, phone=phone, name=request.GET.get('name')).first()
            if guest:
                guest_id = guest.id
            else:
                guest_id = ManeuGuest.objects.create(admin_id=admin_id, phone=phone, name=request.GET.get('name'),time=time).id
            print(guest_id)
            content = report_simple(request)
            report = report_insert(guest_id=guest_id, admin_id=admin_id, phone=phone, name=request.GET.get('name'), time=time, content=content)
            print(report)
            content = order_simple(request.GET.get('content'))
            order = service.order_insert(admin_id=admin_id,
                                         guest_id=guest_id,
                                         report_id=report.id,
                                         time=time,
                                         name=request.GET.get('name'),
                                         phone=phone,
                                         content=content,
                                         remark=request.GET.get('remark'))
            print(order)
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
