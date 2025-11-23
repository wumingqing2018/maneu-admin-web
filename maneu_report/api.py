from django.forms import model_to_dict
from django.http import JsonResponse

from common.simple import report_simple
from common.verify import is_uuid
from maneu_report import service
from maneu.models import ManeuGuest


def search_time(request):
    admin_id = is_uuid(request.session.get('id'))

    if admin_id:
        try:
            data = service.report_search_time(admin_id, request.GET.get('timeS'), request.GET.get('timeE')).values('id', 'guest_id', 'name', 'phone', 'time', 'remark')
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
            data = service.report_search_text(admin_id, request.GET.get('value')).values('id', 'guest_id', 'name', 'phone', 'time','remark')
            content = {'status': True, 'message': admin_id, 'content': list(data)}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)


def delete(request):
    id = is_uuid(request.GET.get('order_id'))
    admin_id = is_uuid(request.session.get('id'))

    if admin_id and id:
        try:
            data = service.report_delete(admin_id=admin_id, id=id)
            content = {'status': True, 'message': '', 'content': {}}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)


def insert(request):
    admin_id = is_uuid(request.session.get('id'))

    if admin_id:
        name = request.GET.get('name')
        time = request.GET.get('time')
        phone = request.GET.get('phone')
        status = 2
        try:
            guest_id = ManeuGuest.objects.create(admin_id=admin_id, time=time, name=name, phone=phone, status=status, sex=request.GET.get('sex'), age=request.GET.get('age'), dfh=request.GET.get('DFH'), em=request.GET.get('EM'), ot=request.GET.get('OT'), remark=request.GET.get('remark')).id

            content = report_simple(request)
            report = service.report_insert(guest_id=guest_id, admin_id=admin_id, time=time, name=name, phone=phone, status=status, content=content)

            content = {'status': True, 'message': '', 'content': {'id': report.id}}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)


def update(request):
    report_id = is_uuid(request.GET.get('report_id'))
    admin_id = is_uuid(request.session.get('id'))
    if admin_id and report_id:
        try:
            content = report_simple(request.GET.get('content'))
            report = service.report_update(id=report_id,
                                           admin_id=admin_id,
                                           name=request.GET.get('name'),
                                           time=request.GET.get('time'),
                                           phone=request.GET.get('phone'),
                                           remark=request.GET.get('remark'),
                                           content=content)
            if report:
                content = {'status': True, 'message': '', 'content': {'id': report_id} }
            else:
                content = {'status': False, 'message': '请输入正确的参数3', 'content': {}}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)


def detail(request):
    report_id = is_uuid(request.GET.get('id'))
    admin_id = is_uuid(request.session.get('id'))
    print(report_id)
    if admin_id and report_id:
        try:
            data = service.report_detail(id=report_id, admin_id=admin_id)
            content = {'status': True, 'message': '', 'content': model_to_dict(data)}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)
