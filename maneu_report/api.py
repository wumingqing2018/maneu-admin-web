"""
maneu_report/api.py

验光报告管理 API（全部 JSON）
"""

import json
import logging
import uuid
from io import BytesIO

from django.db import transaction
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from common.util_decorators import require_admin_id, require_index_id
from common.util_verify import is_call
from maneu_report.service import (
    report_insert, report_detail, report_delete,
    report_update, report_search_time, report_search_data,
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


def _validate_number(value, field_name, errors):
    """
    数值字段轻量校验：
        - 空字符串 → 放行（返回 ''）
        - 可转 float → 放行（返回原字符串）
        - 不可转 float → 记录错误
    """
    if not value:
        return ''
    try:
        float(value)
        return value
    except (ValueError, TypeError):
        errors[field_name] = [{'message': f'{field_name} 必须为数字', 'code': 'invalid'}]
        return ''


def _parse_json(request):
    """
    解析 JSON body，返回 (data, error_response)。
    失败时 error_response 非 None，调用方直接 return 即可。
    """
    try:
        data = json.loads(request.body or '{}')
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, _json_error('无效的 JSON 格式')

    if not isinstance(data, dict):
        return None, _json_error('请求体必须为 JSON 对象')

    return data, None


# ============================================================
# 数值校验字段
# ============================================================
_NUMBER_FIELDS = (
    'pd',
    'od_va', 'od_sph', 'od_cyl', 'od_ax', 'od_pr', 'od_fr',
    'od_al', 'od_ak', 'od_ad', 'od_cct', 'od_lt', 'od_vt',
    'od_bc', 'od_add',
    'os_va', 'os_sph', 'os_cyl', 'os_ax', 'os_pr', 'os_fr',
    'os_al', 'os_ak', 'os_ad', 'os_cct', 'os_lt', 'os_vt',
    'os_bc', 'os_add',
)


# ============================================================
# 新建
# ============================================================
@require_admin_id
def insert(request, admin_id):
    data, err = _parse_json(request)
    if err:
        return err

    time = _get_str(data, 'time')
    name = _get_str(data, 'name')
    phone = _get_str(data, 'phone')
    remark = _get_str(data, 'remark')

    if not time:
        return _json_error('请选择录入时间', status=400)

    optometry = data.get('content') or {}
    if not isinstance(optometry, dict):
        return _json_error('content 格式错误，应为对象', status=400)

    index_id = str(uuid.uuid4())
    report = report_insert(
        admin_id=admin_id,
        index_id=index_id,
        time=time,
        name=name,
        phone=phone,
        remark=remark,
        content=json.dumps(optometry, ensure_ascii=False),
    )
    return _json_ok({
        'index_id': index_id,
        'report_id': report.id,
    }, '创建成功')


# ============================================================
# 详情
# ============================================================

@require_admin_id
@require_index_id
def detail(request, admin_id, index_id):
    """报告详情"""
    try:
        report = report_detail(admin_id=admin_id, index_id=index_id)
    except Exception:
        logger.exception('查询报告失败 index_id=%s', index_id)
        return _json_error('查询失败', status=500)

    if not report:
        return _json_error('报告记录不存在', status=404)
    data = model_to_dict(report)
    return _json_ok({'report': {'ok': True, 'data': data}})


# ============================================================
# 删除
# ============================================================
@require_admin_id
@require_index_id
def delete(request, admin_id, index_id):
    """删除报告"""
    try:
        with transaction.atomic():
            report_delete(admin_id=admin_id, index_id=index_id)
    except Exception:
        logger.exception('删除报告失败 admin_id=%s index_id=%s', admin_id, index_id)
        return _json_error('删除失败，请稍后重试', status=500)

    return _json_ok({}, '删除成功')


# ============================================================
# 更新
# ============================================================

@require_admin_id
@require_index_id
def update(request, admin_id, index_id):
    data, err = _parse_json(request)
    if err:
        return err

    name = _get_str(data, 'name')
    phone = _get_str(data, 'phone')
    remark = _get_str(data, 'remark')

    # content 是 dict，绝不能走 _get_str
    nested = data.get('content') or {}
    if not isinstance(nested, dict):
        return _json_error('content 格式错误，应为对象', status=400)

    # 先确认记录存在
    if not report_detail(admin_id=admin_id, index_id=index_id):
        return _json_error('报告记录不存在', status=404)

    # 数值校验（_NUMBER_FIELDS 是 od_sph/os_sph 这种展平名，eye_data 里是短名）
    errors = {}
    for field in ('age', 'pd'):
        v = nested.get(field, '')
        if v not in (None, ''):
            nested[field] = _validate_number(v, field, errors)

    for eye in ('od', 'os'):
        eye_data = nested.get(eye) or {}
        if not isinstance(eye_data, dict):
            errors[eye] = [{'message': f'{eye} 格式错误，应为对象'}]
            continue
        for field in _NUMBER_FIELDS:
            if not field.startswith(eye + '_'):
                continue
            short = field[len(eye) + 1:]  # 'od_sph' → 'sph'
            v = eye_data.get(short, '')
            if v not in (None, ''):
                eye_data[short] = _validate_number(v, f'{eye}.{short}', errors)
        nested[eye] = eye_data

    if errors:
        return _json_error('参数校验失败', status=400, errors=errors)

    # 序列化为合法 JSON（双引号，ensure_ascii=False 保留中文）
    content_str = json.dumps(nested, ensure_ascii=False)

    try:
        with transaction.atomic():
            report_update(
                admin_id=admin_id,
                index_id=index_id,
                name=name,
                phone=phone,
                remark=remark,
                content=content_str,
            )
    except Exception:
        logger.exception('更新报告失败 index_id=%s', index_id)
        return _json_error('更新失败，请稍后重试', status=500)

    return _json_ok({}, '更新成功')


# ============================================================
# 搜索
# ============================================================
@require_admin_id
def search_time(request, admin_id):
    """按时间范围查报告（JSON）"""
    data, err = _parse_json(request)
    if err:
        return err

    time_start = _get_str(data, 'timeS')
    time_end = _get_str(data, 'timeE')

    if not time_start or not time_end:
        return _json_error('请提供 timeS 和 timeE 参数')

    try:
        qs = report_search_time(admin_id, time_start, time_end)
        return _json_ok(list(qs.values('id', 'name', 'phone', 'time', 'remark')))
    except Exception:
        logger.exception('搜索报告失败 admin_id=%s', admin_id)
        return _json_error('搜索失败', status=500)


@require_admin_id
def search_data(request, admin_id):
    """按关键词查报告（JSON）"""
    data, err = _parse_json(request)
    if err:
        return err

    keyword = _get_str(data, 'value')
    if not keyword:
        return _json_error('请提供搜索关键字')

    try:
        qs = report_search_data(admin_id, keyword)
        return _json_ok(list(qs.values('id', 'name', 'phone', 'time', 'remark')))
    except Exception:
        logger.exception('搜索报告失败 admin_id=%s', admin_id)
        return _json_error('搜索失败', status=500)


# ============================================================
# 二维码
# ============================================================
@require_admin_id
def generate_qr_code(request, admin_id):
    """生成报告验证二维码（JSON）"""
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

    link = f'https://maneu.online/verify_report/?index_id={index_id}'
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
