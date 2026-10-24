"""common/util_response.py — 统一 JSON 响应"""
from django.http import JsonResponse


def json_response(status=True, message='', content=None):
    """统一响应格式：{status, message, content}"""
    return JsonResponse({
        'status': status,
        'message': message,
        'content': content or {},
    })