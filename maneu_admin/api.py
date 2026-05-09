from django.http import JsonResponse

from common.verify import is_uuid
from maneu_admin.service import *


def index(request):
    index_id = is_uuid(request.GET.get('index_id'))

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
        index_id = is_uuid(request.GET.get('index_id'))

        try:
            data = user_update(index_id=index_id, phone=request.GET.get('phone'), nickname=request.GET.get('nickname'),
                               location=request.GET.get('location'))
            content = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}

        return JsonResponse(content)


def search_time(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:

        try:
            data = report_search_time(admin_id=admin_id, timeS=request.GET.get('timeS'), timeE=request.GET.get('timeE'))
            content = {'status': True, 'message': '',
                       'content': list(data.values('id', 'name', 'phone', 'time', 'remark'))}
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
            content = {'status': True, 'message': '',
                       'content': list(data.values('id', 'name', 'phone', 'time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}

    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}
    return JsonResponse(content)
