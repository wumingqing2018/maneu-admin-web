import json
import uuid
from io import BytesIO

import qrcode
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse

from common.simple import filter_store_request_data, extract_report_simple_params, extract_guest_simple_params
from common.verify import is_uuid
from common.jwt_util import _get_admin_id
from maneu_guest.service import *
from maneu_order.service import *
from maneu_report.service import *
from maneu_store.service import store_insert, store_delete


def insert(request):
    time = request.POST.get('time')
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    remark = request.POST.get('remark')
    index_id = uuid.uuid4()
    admin_id = _get_admin_id(request)

    if admin_id:
        try:
            content = filter_store_request_data(request.POST.get('content'))
            data = order_insert(admin_id=admin_id, index_id=index_id, status=3, time=time, name=name, phone=phone,
                                remark=remark, content=content).id
            order = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            order = {'status': False, 'message': str(e), 'content': {}}

        try:
            content = extract_report_simple_params(request)
            data = report_insert(admin_id=admin_id, index_id=index_id, status=3, time=time, name=name, phone=phone,
                                 remark=remark, content=content).id
            report = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            report = {'status': False, 'message': str(e), 'content': {}}

        try:
            content = extract_guest_simple_params(request)
            data = guest_insert(admin_id=admin_id, index_id=index_id, status=3, time=time, name=name, phone=phone,
                                remark=remark, content=content).id
            guest = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            guest = {'status': False, 'message': str(e), 'content': {}}

        try:
            content = filter_store_request_data(request.POST.get('content'))
            data = store_insert(admin_id=admin_id, index_id=index_id, status=3, time=time, name=name, phone=phone,
                                remark=remark, content=content).id
            store = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            store = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '',
                   'content': {'index_id': index_id, 'order': order, 'report': report, 'guest': guest, 'store': store}}
    else:
        content = {'status': False, 'message': '请输入正确的参数',
                   'content': {'index_id': '', 'order': {}, 'report': {}, 'guest': {}, 'store': {}}}
    return JsonResponse(content)


def detail(request):
    admin_id = _get_admin_id(request)
    index_id = is_uuid(request.POST.get('index_id'))
    if admin_id and index_id:
        try:
            order = order_detail(admin_id=admin_id, index_id=index_id)
            content = json.loads(order.content)
            order = {'status': True, 'message': '', 'content': content}
        except Exception as e:
            order = {'status': False, 'message': str(e), 'content': {}}

        try:
            guest = guest_detail(admin_id=admin_id, index_id=index_id)
            content = model_to_dict(guest)
            guest = {'status': True, 'message': '', 'content': content}
        except Exception as e:
            guest = {'status': False, 'message': str(e), 'content': {}}

        try:
            store = guest_detail(admin_id=admin_id, index_id=index_id)
            content = json.loads(store.content)
            store = {'status': True, 'message': '', 'content': content}
        except Exception as e:
            store = {'status': False, 'message': str(e), 'content': {}}

        try:
            report = report_detail(admin_id=admin_id, index_id=index_id)
            content = model_to_dict(report)
            report = {'status': True, 'message': '', 'content': content}
        except Exception as e:
            report = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '',
                   'content': {'order': order, 'guest': guest, 'report': report, 'store': store}}
    else:
        content = {'status': False, 'message': '请输入正确的参数',
                   'content': {'order': {}, 'guest': {}, 'report': {}, 'store': {}}}
    return JsonResponse(content)


def delete(request):
    admin_id = _get_admin_id(request)
    index_id = is_uuid(request.POST.get('index_id'))
    if admin_id and index_id:
        try:
            content = order_delete(admin_id=admin_id, index_id=index_id)
            order = {'status': True, 'message': "", 'content': content}
        except Exception as e:
            order = {'status': False, 'message': str(e), 'content': {}}

        try:
            content = guest_delete(admin_id=admin_id, index_id=index_id)
            guest = {'status': True, 'message': "", 'content': content}
        except Exception as e:
            guest = {'status': False, 'message': str(e), 'content': {}}

        try:
            content = store_delete(admin_id=admin_id, index_id=index_id)
            store = {'status': True, 'message': "", 'content': content}
        except Exception as e:
            store = {'status': False, 'message': str(e), 'content': {}}

        try:
            content = report_delete(admin_id=admin_id, index_id=index_id)
            report = {'status': True, 'message': "", 'content': content}
        except Exception as e:
            report = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '',
                   'content': {'order': order, 'guest': guest, 'report': report, 'store': store}}
    else:
        content = {'status': False, 'message': '请输入正确的参数',
                   'content': {'order': {}, 'guest': {}, 'report': {}, 'store': {}}}
    return JsonResponse(content)


def update(request):
    admin_id = _get_admin_id(request)
    index_id = is_uuid(request.POST.get('index_id'))
    if admin_id and index_id:

        try:
            remark = request.POST.get('orderRemark')
            content = filter_store_request_data(request.POST.get('content'))
            data = order_update_data(admin_id=admin_id, index_id=index_id, content=content, remark=remark)
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
            data = order_search_time(admin_id=admin_id, timeS=request.POST.get('timeS'), timeE=request.POST.get('timeE'))
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
            data = order_search_data(admin_id=admin_id, value=request.POST.get('value'))
            content = {'status': True, 'message': '',
                       'content': list(data.values('id', 'name', 'phone', 'time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}


    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}
    return JsonResponse(content)


def generate_qr_code(request):
    link = 'https://maneu.online/verify_order/?index_id=' + request.POST.get('index_id')

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
