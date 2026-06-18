import uuid
from io import BytesIO

import qrcode
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse

from common.jwt_util import _get_admin_id
from common.simple import extract_guest_simple_params
from common.simple import extract_report_simple_params
from common.verify_util import is_uuid
from maneu_guest.service import *
from maneu_report.service import *


def insert(request):
    admin_id = _get_admin_id(request)
    if admin_id:

        time = request.POST.get('time')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        index_id = uuid.uuid4()

        try:
            content = extract_guest_simple_params(request)
            guest = guest_insert(admin_id=admin_id, index_id=index_id, time=time, name=name, phone=phone, status=2,
                                 content=content, remark=request.POST.get('guestRemark')).id
            guest_id = {'status': True, 'message': guest, 'content': {}}
        except Exception as e:
            guest_id = {'status': False, 'message': str(e), 'content': {}}

        try:
            content = extract_report_simple_params(request)
            report = report_insert(admin_id=admin_id, index_id=index_id, time=time, name=name, phone=phone, status=2,
                                   content=content, remark=request.POST.get('reportRemark')).id
            report_id = {'status': True, 'message': report, 'content': {}}
        except Exception as e:
            report_id = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '',
                   'content': {'index_id': index_id, 'order_id': {}, 'guest_id': guest_id, 'report_id': report_id}}
    else:
        content = {'status': False, 'message': '请输入正确的参数',
                   'content': {'index_id': '', 'order_id': {}, 'guest_id': {}, 'report_id': {}}}
    return JsonResponse(content)


def detail(request):
    admin_id = _get_admin_id(request)
    index_id = is_uuid(request.POST.get('index_id'))
    if admin_id and index_id:

        try:
            data = report_detail(admin_id=admin_id, index_id=index_id)
            report = {'status': True, 'message': '', 'content': model_to_dict(data)}
        except Exception as e:
            report = {'status': False, 'message': str(e), 'content': {}}

        try:
            data = guest_detail(admin_id=admin_id, index_id=index_id)
            guest = {'status': True, 'message': '', 'content': model_to_dict(data)}
        except Exception as e:
            guest = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '',
                   'content': {'order': {}, 'guest': guest, 'report': report}}
    else:
        content = {'status': False, 'message': '请输入正确的参数',
                   'content': {'order': {}, 'guest': {}, 'report': {}}}
    return JsonResponse(content)


def delete(request):
    admin_id = _get_admin_id(request)
    index_id = is_uuid(request.POST.get('index_id'))
    if admin_id and index_id:

        try:
            guest_delete(admin_id=admin_id, index_id=index_id)
            guest_id = {'status': True, 'message': "", 'content': {}}
        except Exception as e:
            guest_id = {'status': False, 'message': str(e), 'content': {}}

        try:
            report_delete(admin_id=admin_id, index_id=index_id)
            report_id = {'status': True, 'message': "", 'content': {}}
        except Exception as e:
            report_id = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '',
                   'content': {'order_id': {}, 'guest_id': guest_id, 'report_id': report_id}}
    else:
        content = {'status': False, 'message': '请输入正确的参数',
                   'content': {'order_id': {}, 'guest_id': {}, 'report_id': {}}}
    return JsonResponse(content)


def update(request):
    admin_id = _get_admin_id(request)
    index_id = is_uuid(request.POST.get('index_id'))
    if admin_id and index_id:

        try:
            content = extract_report_simple_params(request)
            data = report_update(admin_id=admin_id, index_id=index_id, content=content)
            content = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}


    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}
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


def generate_qr_code(request):
    link = 'https://maneu.online/verify_report/?index_id=' + request.POST.get('index_id')

    # 创建二维码对象
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # 将图片存入内存
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # 返回图片响应
    return HttpResponse(buffer, content_type="image/png")
