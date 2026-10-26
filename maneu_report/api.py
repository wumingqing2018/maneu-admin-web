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
    """
    创建验光报告

    请求：application/json
    说明：
        - name / phone / remark 均非必填
        - phone 如果填了，必须是合法手机号
        - time 由后端自动生成
    """
    data, err = _parse_json(request)
    if err:
        return err

    index_id = str(uuid.uuid4())

    errors = {}

    name   = _get_str(data, 'name')
    time = _get_str(data, 'time')
    phone = _get_str(data, 'phone')
    remark = _get_str(data, 'remark')

    # 组装字段
    content = {
        'time': time,
        'name': name,
        'phone': phone,
        'remark': remark,
        'sex': _get_str(data, 'sex'),  # ← 补
        'age': _get_str(data, 'age'),  # ← 补
        'ot': _get_str(data, 'ot'),  # ← 补
        'em': _get_str(data, 'em'),  # ← 补
        'dfh': _get_str(data, 'dfh'),  # ← 补
        'pd': _get_str(data, 'pd'),
    }

    # 数值字段
    for field in _NUMBER_FIELDS:
        if field == 'pd':
            continue
        content[field] = _validate_number(_get_str(data, field), field, errors)

    if errors:
        return _json_error('参数校验失败', status=400, errors=errors)

    logger.info(
        'report.insert admin_id=%s index_id=%s name=%r phone=%r',
        admin_id, index_id, content['name'], content['phone'],
    )

    try:
        with transaction.atomic():
            report = report_insert(
                admin_id=admin_id,
                index_id=index_id,
                status=2,               # ⚠️ 见下文「status 统一」章节
                content=content,
            )
    except Exception:
        logger.exception('创建报告失败 admin_id=%s index_id=%s', admin_id, index_id)
        return _json_error('创建失败，请稍后重试', status=500)

    return _json_ok({
        'index_id':  index_id,
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

    return _json_ok({
        'report': {
            'ok':   True,
            'data': model_to_dict(report),
        },
    })


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
    """
    更新验光报告（JSON）

    字段：name / phone / remark / pd / od_* / os_*
    """
    data, err = _parse_json(request)
    if err:
        return err

    errors = {}

    # 手机号非空才校验
    phone = _get_str(data, 'phone')
    if phone and not is_call(phone):
        errors['phone'] = [{'message': '请输入正确的手机号', 'code': 'invalid'}]

    # 只取实际提供的字段（没传的不更新）
    update_content = {}

    # 文本字段
    for key in ('name', 'phone', 'remark', 'sex', 'age', 'ot', 'em', 'dfh'):
        if key in data:
            update_content[key] = _get_str(data, key)

    # 数值字段
    for field in _NUMBER_FIELDS:
        if field in data:
            update_content[field] = _validate_number(_get_str(data, field), field, errors)

    if errors:
        return _json_error('参数校验失败', status=400, errors=errors)

    if not update_content:
        return _json_error('没有可更新的字段')

    try:
        affected = report_update(
            admin_id=admin_id,
            index_id=index_id,
            content=update_content,
        )
    except Exception:
        logger.exception('更新报告失败 index_id=%s', index_id)
        return _json_error('更新失败，请稍后重试', status=500)

    return _json_ok({'affected_rows': affected}, '更新成功')


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
    time_end   = _get_str(data, 'timeE')

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