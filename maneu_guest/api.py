import uuid
from io import BytesIO

import qrcode
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse


from common.simple import extract_guest_simple_params
from common.verify import is_uuid
from maneu_guest.service import *


def insert(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:
        time = request.GET.get('time')
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        index_id = uuid.uuid4()

        try:
            content = extract_guest_simple_params(request)
            guest_id = guest_insert(admin_id=admin_id, index_id=index_id, time=time, name=name, phone=phone, status=5, content=content, remark=request.GET.get('guestRemark')).id
            guest = {'status': True, 'message': guest_id, 'content': {}}
        except Exception as e:
            guest = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '', 'content': {'index_id': index_id, 'guest_id': guest}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {'index_id': "", 'guest_id': ""}}
    return JsonResponse(content)


def detail(request):
    admin_id = is_uuid(request.session.get('id'))
    index_id = is_uuid(request.GET.get('index_id'))
    if admin_id and index_id:

        try:
            guest = guest_detail(admin_id=admin_id, index_id=index_id)
            content = model_to_dict(guest)
            guest = {'status': True, 'message': '', 'content': content}
        except Exception as e:
            guest = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '', 'content': {'guest': guest}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {'guest': {}}}
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

        content = {'status': True, 'message': '', 'content': {'guest_id': guest_id}}
    else:
        content = {'status': False, 'message': index_id, 'content': {'guest_id': {}}}
    return JsonResponse(content)


def update(request):
    admin_id = is_uuid(request.session.get('id'))
    index_id = is_uuid(request.GET.get('index_id'))
    if admin_id and index_id:

        try:
            data = guest_update(admin_id=admin_id,
                                index_id=index_id,
                                phone=request.GET.get('phone'),
                                name=request.GET.get('name'),
                                time=request.GET.get('time'),
                                sex=request.GET.get('sex'),
                                age=request.GET.get('age'),
                                ot=request.GET.get('ot'),
                                em=request.GET.get('em'),
                                dfh=request.GET.get('dfh'),
                                remark=request.GET.get('guestRemark'))
            guest = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            guest = {'status': False, 'message': str(e), 'content': {}}

        try:
            data = order_update(admin_id=admin_id,
                                index_id=index_id,
                                time=request.GET.get('time'),
                                name=request.GET.get('name'),
                                phone=request.GET.get('phone'),
                                remark=request.GET.get('guestRemark'))

            order = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            order = {'status': False, 'message': str(e), 'content': {}}

        try:
            data = store_update(admin_id=admin_id,
                                index_id=index_id,
                                time=request.GET.get('time'),
                                name=request.GET.get('name'),
                                phone=request.GET.get('phone'),
                                remark=request.GET.get('guestRemark'))

            store = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            store = {'status': False, 'message': str(e), 'content': {}}

        try:
            data = report_update(admin_id=admin_id,
                                 index_id=index_id,
                                 time=request.GET.get('time'),
                                 name=request.GET.get('name'),
                                 phone=request.GET.get('phone'),
                                 remark=request.GET.get('guestRemark'))

            report = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            report = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '',
                   'content': {'order': order, 'guest': guest, 'store': store, 'report': report}}
    else:
        content = {'status': True, 'message': '', 'content': {'order': {}, 'guest': {}, 'store': {}, 'report': {}}}
    return JsonResponse(content)


def search_time(request):
    admin_id = is_uuid(request.session.get('id'))

    if admin_id:
        try:
            data = guest_search_time(admin_id, request.GET.get('timeS'), request.GET.get('timeE'))
            content = {'status': True, 'message': admin_id, 'content': list(data.values('id', 'name', 'phone', 'time', 'status', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)


def search_data(request):
    admin_id = is_uuid(request.session.get('id'))

    if admin_id:
        try:
            data = guest_search_data(admin_id, request.GET.get('value'))
            content = {'status': True, 'message': admin_id, 'content': list(data.values('id', 'name', 'phone', 'time', 'status', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}

    return JsonResponse(content)


def generate_qr_code(request):
    link = 'https://maneu.online/verify_guest/?index_id=' + request.GET.get('index_id')

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
