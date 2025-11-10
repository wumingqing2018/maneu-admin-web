from django.http import JsonResponse

from common.verify import is_uuid
from maneu_admin import service


def detail(request):
    admin_id = is_uuid(request.GET.get('id'))

    if admin_id == request.session.get('id'):
        try:
            userContent = service.user_detail(admin_id=admin_id)
            data = {'nickname': userContent.nickname,
                    'location': userContent.location,
                    'phone': userContent.phone,
                    'time': userContent.time,
                    }
            print(data)

            content = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)


def update(request):
    admin_id = is_uuid(request.GET.get('id'))

    if admin_id == request.session.get('id'):
        try:
            data = service.user_update(admin_id=admin_id, phone=request.GET.get('phone'), nickname=request.GET.get('nickname'), location=request.GET.get('location'))
            content = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {}}

    return JsonResponse(content)
