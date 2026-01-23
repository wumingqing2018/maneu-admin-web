from django.http import JsonResponse

from common.verify import is_uuid
from maneu_report.service import *


def search_time(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:

        try:
            data = report_search_time(admin_id=admin_id, timeS=request.GET.get('timeS'), timeE=request.GET.get('timeE'))
            content = {'status': True, 'message': '', 'content': list(data.values('id','name','phone','time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}

    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}
    return JsonResponse(content)


def search_data(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:

        try:
            data = report_search_data(admin_id=admin_id, value=request.GET.get('value'))
            content = {'status': True, 'message': '', 'content': list(data.values('id','name','phone','time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}

    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}
    return JsonResponse(content)
