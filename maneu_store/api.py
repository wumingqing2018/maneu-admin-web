"""
maneu_store/api.py

零售管理 API（全部 JSON，不用 Form、不依赖 ManeuGuest）
"""

import json
import logging
import uuid
from io import BytesIO

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from common.util_decorators import require_admin_id, require_index_id
from common.util_verify import is_call
from maneu_store.service import (
    store_insert, store_detail, store_delete, store_update_fields,
    store_search_time, store_search_data,
)

logger = logging.getLogger(__name__)


# ============================================================
# 工具
# ============================================================
def _json_error(message, status=400, errors=None):
    body = {'status': False, 'message': message, 'content': {}}
    if errors:
        body['errors'] = errors
    return JsonResponse(body, status=status)


def _json_ok(content=None, message=''):
    return JsonResponse({
        'status': True,
        'message': message,
        'content': content or {},
    })


def _get_str(data, key):
    """从 dict 取字符串（None → ''，其它转 str 后 strip）"""
    v = data.get(key)
    if v is None:
        return ''
    return str(v).strip()


def _parse_json(request):
    """解析 JSON body，返回 (data, error_response)"""
    try:
        data = json.loads(request.body or '{}')
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, _json_error('无效的 JSON 格式')

    if not isinstance(data, dict):
        return None, _json_error('请求体必须为 JSON 对象')

    return data, None


# ============================================================
# 新建
# ============================================================
@require_admin_id
def insert(request, admin_id):
    """
    创建零售记录（JSON）

    请求字段：
        - name / phone / remark ：选填
        - storeContent          ：必填，JSON 字符串或 dict

    说明：
        - time 由后端自动生成
        - status 固定为 1
    """
    data, err = _parse_json(request)
    if err:
        return err

    index_id = str(uuid.uuid4())

    errors = {}



    # storeContent：兼容 dict / list / str
    raw_content = data.get('storeContent')
    if isinstance(raw_content, (dict, list)):
        store_content = json.dumps(raw_content, ensure_ascii=False)
    elif isinstance(raw_content, str):
        store_content = raw_content.strip()
    else:
        store_content = ''

    if not store_content:
        errors['storeContent'] = [{'message': '零售内容不能为空', 'code': 'required'}]

    if errors:
        return _json_error('参数校验失败', status=400, errors=errors)

    name   = _get_str(data, 'name')
    time = _get_str(data, 'time')
    phone = _get_str(data, 'phone')
    remark = _get_str(data, 'remark')

    logger.info(
        'store.insert admin_id=%s index_id=%s name=%r phone=%r',
        admin_id, index_id, name, phone,
    )

    try:
        with transaction.atomic():
            store = store_insert(
                admin_id=admin_id,
                index_id=index_id,
                status=1,
                content={
                    'time':    time,
                    'name':    name,
                    'phone':   phone,
                    'remark':  remark,
                    'content': store_content,   # 内层 JSON 字符串
                },
            )
    except Exception:
        logger.exception('创建零售失败 admin_id=%s index_id=%s', admin_id, index_id)
        return _json_error('创建失败，请稍后重试', status=500)

    return _json_ok({
        'index_id': index_id,
        'store_id': store.id,
    }, '创建成功')


# ============================================================
# 详情
# ============================================================
@require_admin_id
@require_index_id
def detail(request, admin_id, index_id):
    """零售详情（content 已解析为 dict）"""
    try:
        store_obj = store_detail(admin_id=admin_id, index_id=index_id)
    except Exception:
        logger.exception('查询零售失败 index_id=%s', index_id)
        return _json_error('查询失败', status=500)

    if not store_obj:
        return _json_error('零售记录不存在', status=404)

    try:
        content = json.loads(store_obj.content) if store_obj.content else {}
    except json.JSONDecodeError:
        logger.warning('零售内容 JSON 解析失败 index_id=%s', index_id)
        content = {}

    return _json_ok({
        'store': {
            'ok': True,
            'data': {
                'id':      store_obj.id,
                'time':    store_obj.time,
                'name':    store_obj.name,
                'phone':   store_obj.phone,
                'remark':  store_obj.remark,
                'status':  store_obj.status,
                'content': content,
            },
        },
    })


# ============================================================
# 删除
# ============================================================
@require_admin_id
@require_index_id
def delete(request, admin_id, index_id):
    """删除零售记录"""
    try:
        with transaction.atomic():
            store_delete(admin_id=admin_id, index_id=index_id)
    except Exception:
        logger.exception('删除零售失败 admin_id=%s index_id=%s', admin_id, index_id)
        return _json_error('删除失败，请稍后重试', status=500)

    return _json_ok({}, '删除成功')


# ============================================================
# 更新
# ============================================================
@require_admin_id
@require_index_id
def update(request, admin_id, index_id):
    """
    部分更新零售记录（JSON）

    可更新字段：
        - name / phone / remark ：文本
        - storeContent          ：JSON 字符串或 dict（存到 content 字段）

    只更新请求体里实际出现的字段。
    """
    data, err = _parse_json(request)
    if err:
        return err

    errors = {}

    # 手机号非空才校验
    phone = _get_str(data, 'phone')
    if phone and not is_call(phone):
        errors['phone'] = [{'message': '请输入正确的手机号', 'code': 'invalid'}]

    if errors:
        return _json_error('参数校验失败', status=400, errors=errors)

    # 组装待更新字段
    update_fields = {}

    for key in ('name', 'phone', 'remark'):
        if key in data:
            update_fields[key] = _get_str(data, key)

    if 'storeContent' in data:
        raw = data.get('storeContent')
        if isinstance(raw, (dict, list)):
            update_fields['content'] = json.dumps(raw, ensure_ascii=False)
        elif isinstance(raw, str):
            update_fields['content'] = raw.strip()
        else:
            update_fields['content'] = ''

    if not update_fields:
        return _json_error('没有可更新的字段')

    try:
        affected = store_update_fields(
            admin_id=admin_id,
            index_id=index_id,
            fields=update_fields,
        )
    except Exception:
        logger.exception('更新零售失败 index_id=%s', index_id)
        return _json_error('更新失败，请稍后重试', status=500)

    return _json_ok({'affected_rows': affected}, '更新成功')


# ============================================================
# 搜索
# ============================================================
@require_admin_id
def search_time(request, admin_id):
    """按时间范围查零售（JSON）"""
    data, err = _parse_json(request)
    if err:
        return err

    time_start = _get_str(data, 'timeS')
    time_end   = _get_str(data, 'timeE')

    if not time_start or not time_end:
        return _json_error('请提供 timeS 和 timeE 参数')

    try:
        qs = store_search_time(admin_id, time_start, time_end)
        return _json_ok(list(qs.values('id', 'name', 'phone', 'time', 'remark')))
    except Exception:
        logger.exception('搜索零售失败 admin_id=%s', admin_id)
        return _json_error('搜索失败', status=500)


@require_admin_id
def search_data(request, admin_id):
    """按关键词查零售（JSON）"""
    data, err = _parse_json(request)
    if err:
        return err

    keyword = _get_str(data, 'value')
    if not keyword:
        return _json_error('请提供搜索关键字')

    try:
        qs = store_search_data(admin_id, keyword)
        return _json_ok(list(qs.values('id', 'name', 'phone', 'time', 'remark')))
    except Exception:
        logger.exception('搜索零售失败 admin_id=%s', admin_id)
        return _json_error('搜索失败', status=500)


# ============================================================
# 二维码
# ============================================================
@require_admin_id
def generate_qr_code(request, admin_id):
    """
    生成零售验证二维码（JSON）

    请求：{"index_id": "..."}
    响应：image/png（二进制）
    """
    data, err = _parse_json(request)
    if err:
        return err

    index_id = _get_str(data, 'index_id')
    if not index_id:
        return _json_error('缺少 index_id 参数')

    try:
        import qrcode
    except ImportError:
        logger.exception('qrcode 库未安装')
        return _json_error('系统未安装二维码库', status=500)

    link = f'https://maneu.online/verify_store/?index_id={index_id}'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")