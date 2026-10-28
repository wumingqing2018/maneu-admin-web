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
from datetime import datetime
from django.utils import timezone
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
        - time                  ：选填，datetime-local 格式（"YYYY-MM-DDTHH:mm"）
                                  缺省时由后端生成当前时间
        - name / phone / remark ：选填，文本
        - storeContent          ：必填，JSON 字符串或 dict（内层是 [{参数名:参数值}] 数组）

    响应：
        - 成功：{"status": true, "content": {"index_id": "<UUID>", "store_id": <int>}}
        - 失败：{"status": false, "message": "...", "errors": {...}}
    """

    # ============================================================
    # 1) 解析请求体（必须是 JSON 对象）
    # ============================================================
    data, err = _parse_json(request)
    if err:
        return err

    # ============================================================
    # 2) 预处理：生成 index_id + 提取全部字段
    # ============================================================
    # index_id 是业务主键（UUID），和数据库主键 store.id 不同：
    #   - 对外暴露、用于生成二维码链接、查询、删除
    #   - 由后端生成，不信任前端传入
    index_id = str(uuid.uuid4())
    time   = _get_str(data, 'time')
    name   = _get_str(data, 'name')
    phone  = _get_str(data, 'phone')
    remark = _get_str(data, 'remark')

    # ============================================================
    # 3) 逐字段校验
    # ============================================================
    errors = {}

    # ---- 3.1) 时间（选填，缺省由后端补当前时间）----
    # 前端 datetime-local 产出 "YYYY-MM-DDTHH:mm"（带 T 分隔符、无秒）
    # 这里统一转换为 "YYYY-MM-DD HH:MM:SS" 存储，便于后续比较与展示
    if time:
        # 兼容三种格式：
        #   - "2026-10-26T19:54"     （datetime-local 原生）
        #   - "2026-10-26T19:54:00"
        #   - "2026-10-26 19:54:00"  （已转换过的）
        normalized = time.replace('T', ' ')
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M'):
            try:
                parsed_time = datetime.strptime(normalized, fmt)
                # 统一补齐秒位，输出 "YYYY-MM-DD HH:MM:SS"
                time = parsed_time.strftime('%Y-%m-%d %H:%M:%S')
                break
            except ValueError:
                continue
        else:
            # 三种格式都不匹配 → 视为非法输入
            errors['time'] = [{'message': '时间格式错误，应为 YYYY-MM-DDTHH:mm', 'code': 'invalid'}]
    else:
        # 前端未传 time → 用服务器当前时间（遵循业务语义"此刻接单"）
        time = timezone.localtime().replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')

    # ---- 3.3) storeContent（必填，JSON 字符串或 dict/list）----
    # 前端传的是 JSON.stringify([{k: v}]) 的字符串，形如：
    #   '[{"产品系列":"xxx","产品名称":"yyy"}]'
    # 也兼容直接传 dict/list 的情况，统一序列化为字符串
    raw_content = data.get('storeContent')
    if isinstance(raw_content, (dict, list)):
        store_content = json.dumps(raw_content, ensure_ascii=False)
    elif isinstance(raw_content, str):
        store_content = raw_content.strip()
    else:
        store_content = ''

    if not store_content:
        errors['storeContent'] = [{'message': '零售内容不能为空', 'code': 'required'}]
    else:
        # 结构校验：必须是能解析的 JSON，且非空
        try:
            parsed = json.loads(store_content)
            if not isinstance(parsed, (list, dict)) or not parsed:
                errors['storeContent'] = [{'message': '零售内容结构错误', 'code': 'invalid'}]
        except json.JSONDecodeError:
            errors['storeContent'] = [{'message': '零售内容不是合法 JSON', 'code': 'invalid'}]

    # ============================================================
    # 4) 校验汇总：有任意错误直接 400 返回
    # ============================================================
    if errors:
        return _json_error('参数校验失败', status=400, errors=errors)

    # ============================================================
    # 5) 日志（含 index_id，便于后续排查）
    # ============================================================
    logger.info(
        'store.insert admin_id=%s index_id=%s name=%r phone=%r time=%s',
        admin_id, index_id, name, phone, time,
    )

    # ============================================================
    # 6) 落库（事务包裹，避免半写入）
    # ============================================================
    try:
        with transaction.atomic():
            store = store_insert(
                admin_id=admin_id,
                index_id=index_id,      # ← 业务 UUID，用于外链/查询
                status=1,
                content={
                    # 注意：这里 content 内部是一个字典，
                    # 序列化由 store_insert / model 负责（见 service 层实现）
                    'time':    time,
                    'name':    name,
                    'phone':   phone,
                    'remark':  remark,
                    'content': store_content,   # 内层是 "[{...}]" 字符串
                },
            )
    except Exception:
        logger.exception('创建零售失败 admin_id=%s index_id=%s', admin_id, index_id)
        return _json_error('创建失败，请稍后重试', status=500)

    # ============================================================
    # 7) 返回：index_id 是 UUID，store_id 是数据库主键
    # ============================================================
    # ⚠️ 关键修复：原代码 {index_id: store.id} 是错误的
    #   - index_id 是 UUID（业务主键）
    #   - store.id 是 int（数据库主键）
    #   两者语义不同，前端若用返回的 index_id 查详情/生成二维码会 404
    return _json_ok({
        'index_id': index_id,      # ← 正确的业务 UUID
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

    请求字段（全部可选，只更新"实际出现"的字段）：
        - time         ：datetime-local 格式（"YYYY-MM-DDTHH:mm"）
                         出现则更新；缺省则保留原值
        - name         ：文本，允许空串（清空）
        - phone        ：文本，允许空串（清空）
        - remark       ：文本，允许空串（清空）
        - storeContent ：JSON 字符串或 dict/list，非空才更新（不允许清空）

    响应：
        - 成功：{"status": true, "content": {"affected_rows": 1}}
        - 失败：{"status": false, "message": "...", "errors": {...}}
    """

    # ============================================================
    # 1) 解析请求体
    # ============================================================
    data, err = _parse_json(request)
    if err:
        return err

    errors = {}

    # ============================================================
    # 2) 逐字段校验（只校验"出现"的字段，部分更新语义）
    # ============================================================

    # ---- 2.1) time（出现则校验格式并归一化，缺省不动）----
    # 与 insert 保持一致的归一化策略：
    #   输入："2026-10-26T19:54" / "2026-10-26T19:54:00" / "2026-10-26 19:54:00"
    #   输出："YYYY-MM-DD HH:MM:SS"
    time_value = None
    if 'time' in data:
        raw_time = _get_str(data, 'time')
        if raw_time:
            normalized = raw_time.replace('T', ' ')
            for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M'):
                try:
                    parsed_time = datetime.strptime(normalized, fmt)
                    time_value = parsed_time.strftime('%Y-%m-%d %H:%M:%S')
                    break
                except ValueError:
                    continue
            if time_value is None:
                errors['time'] = [{'message': '时间格式错误，应为 YYYY-MM-DDTHH:mm',
                                   'code': 'invalid'}]
        else:
            # 显式传空串 → 视为用户想清空时间？一般不允许。
            # 根据业务：若允许清空，删掉下面两行；若不允许，保留报错。
            errors['time'] = [{'message': '时间不能为空', 'code': 'required'}]

    # ---- 2.3) storeContent（出现则必须非空 + 合法 JSON）----
    # 与 insert 的策略一致：update 不允许"清空产品信息"
    # 因为 insert 时 storeContent 必填，清空后 detail 页会解析失败
    store_content = None
    if 'storeContent' in data:
        raw = data.get('storeContent')
        if isinstance(raw, (dict, list)):
            store_content = json.dumps(raw, ensure_ascii=False)
        elif isinstance(raw, str):
            store_content = raw.strip()
        else:
            store_content = ''

        if not store_content:
            errors['storeContent'] = [{'message': '零售内容不能为空', 'code': 'required'}]
        else:
            try:
                parsed = json.loads(store_content)
                if not isinstance(parsed, (list, dict)) or not parsed:
                    errors['storeContent'] = [{'message': '零售内容结构错误', 'code': 'invalid'}]
            except json.JSONDecodeError:
                errors['storeContent'] = [{'message': '零售内容不是合法 JSON', 'code': 'invalid'}]

    # ============================================================
    # 3) 校验汇总
    # ============================================================
    if errors:
        return _json_error('参数校验失败', status=400, errors=errors)

    # ============================================================
    # 4) 组装待更新字段（保持部分更新语义：只出现才更新）
    # ============================================================
    # ⚠️ 关键：这里的字段名必须与 insert 时 content 字典内的键名一致
    #   insert 时 content = {'time': ..., 'name': ..., 'phone': ..., 'remark': ..., 'content': ...}
    #   update 时 fields 里也用同名 'time'/'name'/'phone'/'remark'/'content'
    update_fields = {}

    if 'name' in data:
        update_fields['name'] = _get_str(data, 'name')

    if 'phone' in data:
        update_fields['phone'] = _get_str(data, 'phone')

    if 'remark' in data:
        update_fields['remark'] = _get_str(data, 'remark')

    if time_value is not None:
        update_fields['time'] = time_value

    if store_content is not None:
        update_fields['content'] = store_content

    if not update_fields:
        return _json_error('没有可更新的字段')

    # ============================================================
    # 5) 落库
    # ============================================================
    logger.info(
        'store.update admin_id=%s index_id=%s fields=%s',
        admin_id, index_id, list(update_fields.keys()),
    )

    try:
        with transaction.atomic():
            affected = store_update_fields(
                admin_id=admin_id,
                index_id=index_id,
                fields=update_fields,
            )
    except Exception:
        logger.exception('更新零售失败 admin_id=%s index_id=%s', admin_id, index_id)
        return _json_error('更新失败，请稍后重试', status=500)

    # ============================================================
    # 6) affected_rows = 0 → 说明 index_id 不存在（或已被删）
    # ============================================================
    if affected == 0:
        return _json_error('零售记录不存在或已被删除', status=404)

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