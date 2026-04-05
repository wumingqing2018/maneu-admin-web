import json
import uuid
from io import BytesIO

import qrcode
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse

from common.simple import store_simple, report_simple, guest_simple
from common.verify import is_uuid
from maneu_guest.service import *
from maneu_order.service import *
from maneu_report.service import *
from maneu_store.service import store_insert


def insert(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:
        time = request.GET.get('time')
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        remark = request.GET.get('remark')
        index_id = uuid.uuid4()


        try:
            data = order_insert(admin_id=admin_id, index_id=index_id, status=3, time=time, name=name, phone=phone, remark=remark, content=content).id
            order = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            order = {'status': False, 'message': str(e), 'content': {}}


        try:
            content = report_simple(request)
            data = report_insert(admin_id=admin_id, index_id=index_id, status=3, time=time, name=name, phone=phone, remark=remark, content=content).id
            report = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            report = {'status': False, 'message': str(e), 'content': {}}


        try:
            content = guest_simple(request)
            data = guest_insert(admin_id=admin_id, index_id=index_id, status=3, time=time, name=name, phone=phone, remark=remark, content=content).id
            guest = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            guest = {'status': False, 'message': str(e), 'content': {}}


        try:
            content = store_simple(request.GET.get('content'))
            data = store_insert(admin_id=admin_id, index_id=index_id, status=3, time=time, name=name, phone=phone, remark=remark, content=content).id
            order = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            order = {'status': False, 'message': str(e), 'content': {}}


        content = {'status': True, 'message': '', 'content':{'index_id': index_id, 'order': order, 'report': report, 'guest': guest}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {'index_id': '', 'order': {}, 'report': {}, 'guest': {}}}
    return JsonResponse(content)


def detail(request):
    admin_id = is_uuid(request.session.get('id'))
    index_id = is_uuid(request.GET.get('index_id'))
    if admin_id and index_id:

        try:
            data = report_detail(admin_id=admin_id, index_id=index_id)
            report_id = {'status': True, 'message': '', 'content': model_to_dict(data)}
        except Exception as e:
            report_id = {'status': False, 'message': str(e), 'content': {}}

        try:
            order = order_detail(admin_id=admin_id, index_id=index_id)
            content = {'time': order.time, 'name': order.name, 'phone': order.phone, 'remark': order.remark, 'content': json.loads(order.content),}
            order_id = {'status': True, 'message': '', 'content': content}
        except Exception as e:
            order_id = {'status': False, 'message': str(e), 'content': {}}

        try:
            data = guest_detail(admin_id=admin_id, index_id=index_id)
            guest_id = {'status': True, 'message': '', 'content': model_to_dict(data)}
        except Exception as e:
            guest_id = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '', 'content':{'order_id': order_id, 'guest_id': guest_id, 'report_id': report_id}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {'order_id': {}, 'guest_id': {}, 'report_id': {}}}
    return JsonResponse(content)


def delete(request):
    admin_id = is_uuid(request.session.get('id'))
    index_id = is_uuid(request.GET.get('index_id'))
    if admin_id and index_id:

        try:
            guest_delete(admin_id=admin_id, index_id=index_id)
            guest_id = {'status': True, 'message': "", 'content': {}}
        except Exception as e:
            guest_id = {'status': False, 'message': str(e), 'content': {}}

        try:
            order_delete(admin_id=admin_id, index_id=index_id)
            order_id = {'status': True, 'message': "", 'content': {}}
        except Exception as e:
            order_id = {'status': False, 'message': str(e), 'content': {}}

        try:
            report_delete(admin_id=admin_id, index_id=index_id)
            report_id = {'status': True, 'message': "", 'content': {}}
        except Exception as e:
            report_id = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '', 'content':{'order_id': order_id, 'guest_id': guest_id, 'report_id': report_id}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {'order_id': {}, 'guest_id': {}, 'report_id': {}}}
    return JsonResponse(content)


def update(request):
    admin_id = is_uuid(request.session.get('id'))
    index_id = is_uuid(request.GET.get('index_id'))
    if admin_id and index_id:

        try:
            remark = request.GET.get('orderRemark')
            content = store_simple(request.GET.get('content'))
            data = order_update_data(admin_id=admin_id, index_id=index_id, content=content, remark=remark)
            content = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}

    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}
    return JsonResponse(content)


def search_time(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:
        try:
            data = order_search_time(admin_id=admin_id, timeS=request.GET.get('timeS'), timeE=request.GET.get('timeE'))
            content = {'status': True, 'message': '', 'content': list(data.values('id', 'name', 'phone', 'time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}

    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}
    return JsonResponse(content)


def search_data(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:

        try:
            data = order_search_data(admin_id=admin_id, value=request.GET.get('value'))
            content = {'status': True, 'message': '', 'content': list(data.values('id', 'name', 'phone', 'time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}

    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}
    return JsonResponse(content)


def generate_qr_code(request):
    link='https://maneu.online/verify_order/?order_id='+request.GET.get('index_id')
    print(link)

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