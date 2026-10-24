"""common/util_decorators.py — 视图装饰器"""
import json
from functools import wraps

from common.util_jwt import get_admin_id
from common.util_verify import is_uuid
from common.util_response import json_response


def _extract_param(request, key):
    """兼容 form 和 JSON body"""
    if request.content_type == 'application/json':
        try:
            return json.loads(request.body or '{}').get(key)
        except json.JSONDecodeError:
            return None
    return request.POST.get(key)


def require_admin_id(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        admin_id = get_admin_id(request)
        if not admin_id:
            return json_response(False, '未授权或管理员ID无效')
        kwargs['admin_id'] = admin_id
        return func(request, *args, **kwargs)
    return wrapper


def require_index_id(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        index_id = is_uuid(_extract_param(request, 'index_id'))
        if not index_id:
            return json_response(False, '缺少有效的 index_id 参数')
        kwargs['index_id'] = index_id
        return func(request, *args, **kwargs)
    return wrapper