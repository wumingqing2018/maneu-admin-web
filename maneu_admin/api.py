from django.http import JsonResponse

from common.jwt_util import _get_admin_id
from common.verify_util import is_uuid
from maneu_admin.service import *


def index(request):
    index_id = is_uuid(request.POST.get('index_id'))

    try:
        userContent = user_detail(index_id=index_id)
        data = {'nickname': userContent.nickname,
                'location': userContent.location,
                'phone': userContent.phone,
                'time': userContent.time,
                }
        print(data)

        content = {'status': True, 'message': '', 'content': data}
    except Exception as e:
        content = {'status': False, 'message': str(e), 'content': {}}

    return JsonResponse(content)


def update(request):
    index_id = is_uuid(request.POST.get('index_id'))

    try:
        data = user_update(index_id=index_id, phone=request.POST.get('phone'), nickname=request.POST.get('nickname'),
                           location=request.POST.get('location'))
        content = {'status': True, 'message': '', 'content': data}
    except Exception as e:
        content = {'status': False, 'message': str(e), 'content': {}}

    return JsonResponse(content)


def search_time(request):
    admin_id = _get_admin_id(request)
    if admin_id:

        try:
            data = report_search_time(admin_id=admin_id, timeS=request.POST.get('timeS'), timeE=request.POST.get('timeE'))
            content = {'status': True, 'message': '',
                       'content': list(data.values('id', 'name', 'phone', 'time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}

    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}
    return JsonResponse(content)


def search_data(request):
    admin_id = _get_admin_id(request)
    if admin_id:

        try:
            data = report_search_data(admin_id=admin_id, value=request.POST.get('value'))
            content = {'status': True, 'message': '',
                       'content': list(data.values('id', 'name', 'phone', 'time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}

    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}
    return JsonResponse(content)
