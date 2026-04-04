import json
import uuid
from io import BytesIO

import qrcode
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse

from common.simple import guest_simple
from common.verify import is_uuid
from maneu_guest.service import *
from maneu_store.service import *


def qrcode(request):
    link = 'https://maneu.online/get_verify/?store_id=' + request.GET.get('index_id')
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


def insert(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:
        time = request.GET.get('time')
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        index_id = uuid.uuid4()


        try:
            content1 = guest_simple(request)
            content2 = guest_insert(admin_id=admin_id, index_id=index_id, time=time, name=name, phone=phone, status=3, content=content1, remark=request.GET.get('guestRemark')).id
            guest = {'status': True, 'message': '', 'content': content2}
        except Exception as e:
            guest = {'status': False, 'message': str(e), 'content': {}}


        try:
            content1 = store_insert(admin_id=admin_id, index_id=index_id, time=time, name=name, phone=phone,
                                 Class=request.GET.get('Class'), brand=request.GET.get('brand'),
                                 model=request.GET.get('model'), price=request.GET.get('price'),
                                 parameter=request.GET.get('parameter'), content=request.GET.get('storeContent')).id
            store = {'status': True, 'message': content1, 'content': {}}
        except Exception as e:
            store = {'status': False, 'message': str(e), 'content': {}}


        content = {'status': True, 'message': '', 'content': {'index_id': index_id}}
    else:
        content = {'status': False, 'message': '请输入正确的参数', 'content': {'index_id': ''}}
    return JsonResponse(content)


def detail(request):
    admin_id = is_uuid(request.session.get('id'))
    index_id = is_uuid(request.GET.get('index_id'))

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
    admin_id = is_uuid(request.session.get('id'))
    index_id = is_uuid(request.GET.get('index_id'))
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


def update_time(request):
    admin_id = is_uuid(request.session.get('id'))
    index_id = is_uuid(request.GET.get('index_id'))
    if admin_id and index_id:


        try:
            data = guest_update_data(admin_id=admin_id,
                                     index_id=index_id,
                                     time=request.GET.get('time'),
                                     name=request.GET.get('name'),
                                     phone=request.GET.get('phone'),
                                     remark=request.GET.get('remark'),
                                     dfh=request.GET.get('dfh'),
                                     sex=request.GET.get('sex'),
                                     age=request.GET.get('age'),
                                     ot=request.GET.get('ot'),
                                     em=request.GET.get('em'))
            guest = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            guest = {'status': False, 'message': str(e), 'content': {}}


        try:
            data = store_update_time(admin_id=admin_id,
                                     index_id=index_id,
                                     phone=request.GET.get('phone'),
                                     time=request.GET.get('time'),
                                     name=request.GET.get('name'))
            store = {'status': True, 'message': '', 'content': data}
        except Exception as e:
            store = {'status': False, 'message': str(e), 'content': {}}


        content = {'status': True, 'message': '', 'content': {'store': store, 'guest': guest}}
    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {'store': {}, 'guest': {}}}

    return JsonResponse(content)


def update_data(request):
    admin_id = is_uuid(request.session.get('id'))
    index_id = is_uuid(request.GET.get('index_id'))
    if admin_id and index_id:


        try:
            data = store_update_data(admin_id=admin_id, index_id=index_id, content=request.GET.get('content'))
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
            data = store_search_time(admin_id=admin_id, timeS=request.GET.get('timeS'), timeE=request.GET.get('timeE'))
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
            data = store_search_data(admin_id=admin_id, value=request.GET.get('value'))
            content = {'status': True, 'message': '',
                       'content': list(data.values('id', 'name', 'phone', 'time', 'remark'))}
        except Exception as e:
            content = {'status': False, 'message': str(e), 'content': {}}


    else:
        content = {'status': False, 'message': '参数错误请确认', 'content': {}}
    return JsonResponse(content)

