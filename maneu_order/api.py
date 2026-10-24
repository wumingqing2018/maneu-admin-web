"""
maneu_order/api.py

订单管理 API（全部 JSON，不使用 Form）
"""
import uuid
import json
import logging
from io import BytesIO

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from common.util_decorators import require_admin_id, require_index_id
from maneu_order.service import (
    order_insert, order_delete, order_detail,
    order_update_data, order_search_data, order_search_time,
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
    v = data.get(key)
    if v is None:
        return ''
    return str(v).strip()


def _parse_json(request):
    try:
        data = json.loads(request.body or '{}')
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, _json_error('无效的 JSON 格式')

    if not isinstance(data, dict):
        return None, _json_error('请求体必须为 JSON 对象')

    return data, None


# ============================================================
# 产品明细校验（适配眼镜订单格式 item_type / unit_price）
# ============================================================
_VALID_ITEM_TYPES = {'frame', 'lens', 'accessory', 'service'}


def _validate_products(raw):
    """
    校验产品明细数组（眼镜订单格式）

    每项字段：
        item_type  - 必填：frame / lens / accessory / service
        side       - 选填：OD / OS / OU（仅镜片有意义）
        brand      - 镜架 / 镜片必填
        model      - 全部必填（配件/服务为名称）
        color      - 镜架必填
        material   - 选填
        spec       - 选填
        quantity   - 必填，≥1
        unit_price - 必填，≥0（兼容 price）
        remark     - 选填
    """
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            return None, [{'message': 'products 格式错误（非合法 JSON）', 'code': 'invalid'}]

    if not isinstance(raw, list):
        return None, [{'message': 'products 必须为数组', 'code': 'invalid'}]

    if len(raw) == 0:
        return None, [{'message': '至少需要一条产品信息', 'code': 'required'}]

    cleaned, errors = [], []

    for idx, item in enumerate(raw):
        if not isinstance(item, dict):
            errors.append({'index': idx, 'message': f'第 {idx+1} 项格式错误（必须是对象）'})
            continue

        item_type  = str(item.get('item_type', '') or '').strip().lower()
        side       = str(item.get('side', '')      or '').strip().upper()
        brand      = str(item.get('brand', '')     or '').strip()
        model      = str(item.get('model', '')     or '').strip()
        color      = str(item.get('color', '')     or '').strip()
        material   = str(item.get('material', '')  or '').strip()
        spec       = str(item.get('spec', '')      or '').strip()
        remark     = str(item.get('remark', '')    or '').strip()
        quantity   = item.get('quantity', 1)
        unit_price = item.get('unit_price', item.get('price'))

        item_msgs = []

        # 类型
        if not item_type:
            item_msgs.append('产品类型必填（frame/lens/accessory/service）')
        elif item_type not in _VALID_ITEM_TYPES:
            item_msgs.append(f'无效的产品类型：{item_type}')

        # 数量
        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
        except (TypeError, ValueError):
            item_msgs.append('数量必须 ≥ 1')
            quantity = 1

        # 单价
        try:
            unit_price = float(unit_price)
            if unit_price < 0:
                item_msgs.append('单价不能为负')
        except (TypeError, ValueError):
            item_msgs.append('单价必须为数字')
            unit_price = 0.0

        # 类型专属必填
        if item_type == 'frame':
            if not brand:
                item_msgs.append('镜架必须填品牌')
            if not model:
                item_msgs.append('镜架必须填型号')
            if not color:
                item_msgs.append('镜架必须填颜色')
            side = ''
        elif item_type == 'lens':
            if not brand:
                item_msgs.append('镜片必须填品牌')
            if side and side not in ('OD', 'OS', 'OU'):
                item_msgs.append('镜片 side 只能是 OD / OS / OU')
        elif item_type in ('accessory', 'service'):
            if not model:
                item_msgs.append('名称必填')
            side = ''

        if item_msgs:
            errors.append({'index': idx, 'message': f'第 {idx+1} 行：' + '，'.join(item_msgs)})
        else:
            cleaned.append({
                'item_type':  item_type,
                'side':       side,
                'brand':      brand,
                'model':      model,
                'color':      color,
                'material':   material,
                'spec':       spec,
                'quantity':   quantity,
                'unit_price': unit_price,
                'remark':     remark,
            })

    if errors:
        return None, errors
    return cleaned, []


# ============================================================
# 新建（只创建 order）
# ============================================================
@require_admin_id
def insert(request, admin_id):
    """
    创建订单

    请求 JSON：
        name / phone / remark - 选填
        products              - 必填，数组
            每项：{item_type, side, brand, model, color, material, spec, quantity, unit_price, remark}
    """
    data, err = _parse_json(request)
    if err:
        return err

    errors = {}

    # 产品明细
    cleaned_products, product_errors = _validate_products(data.get('products'))
    if product_errors:
        errors['products'] = product_errors

    if errors:
        return _json_error('参数校验失败', status=400, errors=errors)

    now = timezone.localtime().replace(microsecond=0)
    index_id = str(uuid.uuid4())
    phone = _get_str(data, 'phone')
    name   = _get_str(data, 'name')
    remark = _get_str(data, 'remark')

    logger.info(
        'order.insert admin_id=%s index_id=%s name=%r phone=%r products=%d',
        admin_id, index_id, name, phone, len(cleaned_products),
    )

    try:
        with transaction.atomic():
            order = order_insert(
                admin_id=admin_id,
                index_id=index_id,
                status=3,
                content={
                    'name':     name,
                    'time':     now,
                    'phone':    phone,
                    'remark':   remark,
                    'products': cleaned_products,
                },
            )
    except Exception:
        logger.exception('创建订单失败 admin_id=%s index_id=%s', admin_id, index_id)
        return _json_error('创建失败，请稍后重试', status=500)

    return _json_ok({
        'index_id': index_id,
        'order_id': order.id,
    }, '创建成功')


# ============================================================
# 详情
# ============================================================
@require_admin_id
@require_index_id
def detail(request, index_id, admin_id):
    """订单详情"""
    try:
        obj = order_detail(admin_id=admin_id, index_id=index_id)
        if not obj:
            return _json_error('订单不存在', status=404)

        try:
            products = json.loads(obj.content or '[]')
        except json.JSONDecodeError:
            products = []

        return _json_ok({
            'order': {
                'ok': True,
                'data': {
                    'id':       obj.id,
                    'time':     obj.time,
                    'name':     obj.name,
                    'phone':    obj.phone,
                    'remark':   obj.remark,
                    'status':   obj.status,
                    'products': products,
                },
            },
        })
    except Exception:
        logger.exception('订单查询失败 index_id=%s', index_id)
        return _json_error('查询失败', status=500)


# ============================================================
# 删除
# ============================================================
@require_admin_id
@require_index_id
def delete(request, index_id, admin_id):
    """删除订单"""
    try:
        with transaction.atomic():
            order_delete(admin_id=admin_id, index_id=index_id)
    except Exception:
        logger.exception('删除失败 admin_id=%s index_id=%s', admin_id, index_id)
        return _json_error('删除失败，请稍后重试', status=500)

    return _json_ok({}, '删除成功')


# ============================================================
# 更新
# ============================================================
@require_admin_id
@require_index_id
def update(request, index_id, admin_id):
    """更新订单（remark / products）"""
    data, err = _parse_json(request)
    if err:
        return err

    errors = {}
    update_content = {}

    if 'remark' in data:
        update_content['remark'] = _get_str(data, 'remark')

    if 'products' in data:
        cleaned_products, product_errors = _validate_products(data.get('products'))
        if product_errors:
            errors['products'] = product_errors
        else:
            update_content['products'] = cleaned_products

    if errors:
        return _json_error('参数校验失败', status=400, errors=errors)

    if not update_content:
        return _json_error('没有可更新的字段')

    try:
        order_update_data(
            admin_id=admin_id,
            index_id=index_id,
            content=update_content,
        )
    except Exception:
        logger.exception('更新订单失败 index_id=%s', index_id)
        return _json_error('更新失败，请稍后重试', status=500)

    return _json_ok({}, '更新成功')


# ============================================================
# 搜索
# ============================================================
@require_admin_id
def search_time(request, admin_id):
    data, err = _parse_json(request)
    if err:
        return err

    time_s = _get_str(data, 'timeS')
    time_e = _get_str(data, 'timeE')
    if not time_s or not time_e:
        return _json_error('请提供 timeS 和 timeE 参数')

    try:
        qs = order_search_time(admin_id=admin_id, timeS=time_s, timeE=time_e)
        return _json_ok(list(qs.values('id', 'name', 'phone', 'time', 'remark')))
    except Exception:
        logger.exception('搜索订单失败 admin_id=%s', admin_id)
        return _json_error('搜索失败', status=500)


@require_admin_id
def search_data(request, admin_id):
    data, err = _parse_json(request)
    if err:
        return err

    value = _get_str(data, 'value')
    if not value:
        return _json_error('请提供搜索关键字')

    try:
        qs = order_search_data(admin_id=admin_id, value=value)
        return _json_ok(list(qs.values('id', 'name', 'phone', 'time', 'remark')))
    except Exception:
        logger.exception('搜索订单失败 admin_id=%s', admin_id)
        return _json_error('搜索失败', status=500)


# ============================================================
# 二维码
# ============================================================
@require_admin_id
def generate_qr_code(request, admin_id):
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

    link = f'https://maneu.online/verify_order/?index_id={index_id}'
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