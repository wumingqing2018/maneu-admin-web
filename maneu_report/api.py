from uuid import uuid4

from django.forms import model_to_dict
from django.http import JsonResponse

from common.simple import report_simple
from common.verify import is_uuid
from maneu_guest.service import ManeuGuest_get
from maneu_report import service


def search_time(request):
    admin_id = is_uuid(request.session.get('id'))

    if admin_id:
        try:
            data = service.report_search_time(admin_id, request.GET.get('timeS'), request.GET.get('timeE')).values('id', 'guest_id', 'name', 'phone', 'time', 'remark')
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
            data = service.report_search_text(admin_id, request.GET.get('value')).values('id', 'guest_id', 'name', 'phone', 'time','remark')
            content = {'status': True, 'message': admin_id, 'content': list(data), 'mark': uuid4()}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}, 'mark': uuid4()}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)


def delete(request):
    id = is_uuid(request.GET.get('id'))
    admin_id = is_uuid(request.session.get('id'))

    if admin_id and id:
        try:
            data = service.report_delete(admin_id=admin_id, id=id)
            content = {'status': True, 'message': '', 'content': {}, 'mark': uuid4()}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}, 'mark': uuid4()}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)


def insert(request):
    admin_id = is_uuid(request.session.get('id'))

    if admin_id:
        content = report_simple(request)
        try:
            guest_id = ManeuGuest_get(admin_id=admin_id, phone=request.GET.get('phone')).id
            report = service.report_insert(admin_id=admin_id,
                                           guest_id=guest_id,
                                           time=request.GET.get('time'),
                                           name=request.GET.get('name'),
                                           phone=request.GET.get('phone'),
                                           remark=request.GET.get('remark'),
                                           content=content)
            content = {'status': True, 'message': '', 'content': {'id': report.id}, 'mark': uuid4()}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}, 'mark': uuid4()}
    else:
        content = {'status': False, 'message': '请输入正确的参数1', 'content': {}}

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
                content = {'status': True, 'message': '', 'content': {'id': report_id} , 'mark': uuid4()}
            else:
                content = {'status': False, 'message': '请输入正确的参数3', 'content': {}}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}, 'mark': uuid4()}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)


def detail(request):
    report_id = is_uuid(request.GET.get('id'))
    admin_id = is_uuid(request.session.get('id'))
    if admin_id and report_id:
        try:
            data = service.report_detail(id=report_id, admin_id=admin_id)
            content = {'status': True, 'message': '', 'content': model_to_dict(data), 'mark': uuid4()}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}, 'mark': uuid4()}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)
