import json
import uuid
from io import BytesIO

import qrcode
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse

from common.simple import extract_guest_simple_params
from common.verify import is_uuid
from common.jwt_util import _get_admin_id
from maneu_guest.service import *
from maneu_store.service import *


def generate_qr_code(request):
    link = 'https://maneu.online/verify_store/?index_id=' + request.POST.get('index_id')

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


def insert(request):
    admin_id = _get_admin_id(request)
    if admin_id:
        time = request.POST.get('time')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        remark = request.POST.get('remark')
        index_id = uuid.uuid4()

        try:
            content = extract_guest_simple_params(request)
            data = guest_insert(admin_id=admin_id, index_id=index_id, time=time, name=name, phone=phone, status=1,
                                content=content, remark=remark).id
            guest = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            guest = {'status': False, 'message': str(e), 'content': {}}

        try:
            content = request.POST.get('storeContent')
            data = store_insert(admin_id=admin_id, index_id=index_id, time=time, name=name, phone=phone, status=1,
                                content=content, remark=remark).id
            store = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            store = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '', 'content': {'index_id': index_id, 'store': store, 'guest': guest}}
    else:
        content = {'status': False, 'message': '请输入正确的参数',
                   'content': {'index_id': '', 'store': {}, 'guest': {}}}
    return JsonResponse(content)


def detail(request):
    admin_id = _get_admin_id(request)
    index_id = is_uuid(request.POST.get('index_id'))
    if admin_id and index_id:

        try:
            data = store_detail(admin_id=admin_id, index_id=index_id)
            store = {'status': True, 'message': '', 'content': json.loads(data.content)}
        except Exception as e:
            store = {'status': False, 'message': str(e), 'content': {}}

        try:
            data = guest_detail(admin_id=admin_id, index_id=index_id)
            guest = {'status': True, 'message': '', 'content': model_to_dict(data)}
        except Exception as e:
            guest = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '', 'content': {'store': store, 'guest': guest}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {'store': {}, 'guest': {}}}
    return JsonResponse(content)


def delete(request):
    admin_id = _get_admin_id(request)
    index_id = is_uuid(request.POST.get('index_id'))
    if admin_id and index_id:

        try:
            guest = {'status': True, 'message': "", 'content': guest_delete(admin_id=admin_id, index_id=index_id)}
        except Exception as e:
            guest = {'status': False, 'message': str(e), 'content': {}}

        try:
            store = {'status': True, 'message': "", 'content': store_delete(admin_id=admin_id, index_id=index_id)}
        except Exception as e:
            store = {'status': False, 'message': str(e), 'content': {}}

        content = {'status': True, 'message': '', 'content': {'store': store, 'guest': guest}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {'store': {}, 'guest': {}}}
    return JsonResponse(content)


def update(request):
    admin_id = _get_admin_id(request)
    index_id = is_uuid(request.POST.get('index_id'))
    if admin_id and index_id:
        print(request.POST.get('storeContent'))

        try:
            data = store_update(admin_id=admin_id, index_id=index_id, content=request.POST.get('storeContent'))
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
            data = store_search_time(admin_id=admin_id, timeS=request.POST.get('timeS'), timeE=request.POST.get('timeE'))
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
            data = store_search_data(admin_id=admin_id, value=request.POST.get('value'))
            content = {'status': True, 'message': '',
                       'content': list(data.values('id', 'name', 'phone', 'time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}


    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}
    return JsonResponse(content)
