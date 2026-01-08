from django.forms import model_to_dict
from django.http import JsonResponse

from common.simple import report_simple
from common.verify import is_uuid
from maneu_guest.service import *
from maneu_report.service import *


def insert(request):
    admin_id = is_uuid(request.session.get('id'))

    if admin_id:
        name = request.GET.get('name')
        time = request.GET.get('time')
        phone = request.GET.get('phone')
        status = 2
        try:
            guest_id = guest_insert(admin_id=admin_id,
                                    time=time,
                                    name=name,
                                    phone=phone,
                                    status=status,
                                    sex=request.GET.get('sex'),
                                    age=request.GET.get('age'),
                                    dfh=request.GET.get('DFH'),
                                    em=request.GET.get('EM'),
                                    ot=request.GET.get('OT'),
                                    remark=request.GET.get('guestRemark')).id

            content = report_simple(request)
            report = report_insert(admin_id=admin_id,
                                   guest_id=guest_id,
                                   time=time,
                                   name=name,
                                   phone=phone,
                                   status=status,
                                   content=content,
                                   remark=request.GET.get('reportRemark'))

            content = {'status': True, 'message': '', 'content': {'id': report.id}}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}
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

        report_id = is_uuid(request.GET.get('report_id'))
        if report_id:
            try:
                data = report_detail(admin_id=admin_id, report_id=report_id)
                report_id = {'status': True, 'message': '', 'content': model_to_dict(data)}
            except Exception as e:
                report_id = {'status': False, 'message': str(e), 'content': {}}
        else:
            report_id = {'status': False, 'message': '请输入正确的参数', 'content': {}}

        content = {'status': True, 'message': '', 'content':{'report_id': report_id, 'guest_id': guest_id}}
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

        report_id = is_uuid(request.GET.get('report_id'))
        if report_id:
            try:
                report_id = report_delete(admin_id=admin_id, report_id=report_id)[0]
            except Exception as e:
                report_id = 0
        else:
            report_id = 0

        content = {'status': True, 'message': '', 'content': {'guest_id': guest_id, 'report_id': report_id}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {'guest_id': {}, 'order_id': {}, 'report_id': {}}}
    return JsonResponse(content)


def search_time(request):
    admin_id = is_uuid(request.session.get('id'))

    if admin_id:
        try:
            data = report_search_time(admin_id, request.GET.get('timeS'), request.GET.get('timeE'))
            content = {'status': True, 'message': '', 'content': list(data.values('id','guest_id','name','phone','time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)


def search_data(request):
    admin_id = is_uuid(request.session.get('id'))

    if admin_id:
        try:
            data = report_search_data(admin_id, request.GET.get('value'))
            content = {'status': True, 'message': '', 'content': list(data.values('id','guest_id','name','phone','time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)


def update_time(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:

        guest_id = is_uuid(request.GET.get('guest_id'))
        if guest_id:
            try:
                data = guest_update_time(admin_id=admin_id, guest_id=guest_id, time=request.GET.get('time'))
                guest_id = {'status': True, 'message': '', 'content': data}
            except Exception as e:
                guest_id = {'status': False, 'message': str(e), 'content': {}}
        else:
            guest_id = {'status': False, 'message': 'order_id 更新有误', 'content': {}}

        report_id = is_uuid(request.GET.get('report_id'))
        if report_id:
            try:
                data = report_update_time(admin_id=admin_id, report_id=report_id, time=request.GET.get('time'))
                report_id = {'status': True, 'message': '', 'content': data}
            except Exception as e:
                report_id = {'status': False, 'message': str(e), 'content': {}}
        else:
            report_id = {'status': False, 'message': 'order_id 更新有误', 'content': {}}

        content = {'status': True, 'message': '', 'content': {'guest_id': guest_id, 'report_id': report_id}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {'guest_id': {}, 'order_id': {}, 'report_id': {}}}

    return JsonResponse(content)


def update_data(request):
    report_id = is_uuid(request.GET.get('report_id'))
    admin_id = is_uuid(request.session.get('id'))
    if admin_id and report_id:
        try:
            content = report_simple(request)
            report = report_update_data(report_id=report_id,
                                        admin_id=admin_id,
                                        name=request.GET.get('name'),
                                        phone=request.GET.get('phone'),
                                        remark=request.GET.get('reportRemark'),
                                        content=content)
            if report:
                content = {'status': True, 'message': '', 'content': {'report_id': report_id}}
            else:
                content = {'status': False, 'message': '请输入正确的参数3', 'content': {}}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)
