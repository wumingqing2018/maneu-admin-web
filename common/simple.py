import json
from typing import Dict, Any, List

from django.http import HttpRequest


def extract_guest_simple_params(request: HttpRequest) -> Dict[str, str]:
    """
    从 GET 请求中提取访客（guest）的简单参数。
    预定义字段：age, sex, dfh, ot, em。如果请求中缺少某个字段，则保留空字符串。

    Args:
        request: Django HTTP 请求对象。

    Returns:
        dict: 包含五个字段的字典，键为 'age', 'sex', 'dfh', 'ot', 'em'。
    """
    # 预定义的简单参数字典，初始值为空字符串
    simple = {
        'age': '',
        'sex': '',
        'dfh': '',
        'ot': '',
        'em': ''
    }

    # 遍历所有键，尝试从 GET 参数中获取并覆盖
    for key in simple.keys():
        try:
            value = request.GET.get(key)
            if value is not None:
                simple[key] = value
        except Exception:
            # 忽略任何异常（例如 request.GET 不可用），保持原值
            pass

    return simple


def filter_store_request_data(raw_request_body: str) -> str:
    """
    处理存储请求的 JSON 数据，过滤掉与默认结构相同的条目。
    预期输入是一个包含多个对象的数组，函数会移除那些对象结构与预定义 simple 字典完全一致的条目，
    然后返回剩余条目的 JSON 数组字符串。

    Args:
        raw_request_body: HTTP 请求体的原始字符串，应为一个 JSON 数组。

    Returns:
        str: 过滤后的 JSON 数组字符串。如果输入无效或解析失败，返回空数组 '[]'。
    """
    # 默认的简单结构，用于过滤匹配的条目
    simple_template = {
        'arg10': '',
        'arg11': '',
        'arg12': '',
        'arg13': '',
        'arg14': ''
    }

    try:
        # 将请求体解析为 Python 对象（期望是列表）
        request_data: List[Dict[str, Any]] = json.loads(raw_request_body)
    except json.JSONDecodeError:
        # 如果 JSON 解析失败，返回空数组
        return "[]"

    # 筛选出与 simple_template 结构不同的条目
    filtered_data = [
        item for item in request_data
        if item != simple_template  # 只保留不等于模板的条目
    ]

    # 将筛选结果转为 JSON 字符串并返回
    return json.dumps(filtered_data)


def extract_report_simple_params(request: HttpRequest) -> Dict[str, Any]:
    """
    从 GET 请求中提取报告（report）的简单参数。
    预定义了一组眼科检查相关字段（左右眼各项指标），默认值为 None 或 0.00。
    如果请求中包含相应参数，则覆盖默认值。

    Args:
        request: Django HTTP 请求对象。

    Returns:
        dict: 包含所有报告字段的字典，键名如 'plan', 'pd', 'os_al' 等。
    """
    # 定义报告的默认值模板
    simple = {
        'plan': None,
        'pd': None,
        'os_al': None,
        'os_ak': None,
        'os_ax': 0.00,
        'os_ad': None,
        'os_add': 0.00,
        'os_bc': None,
        'os_cyl': 0.00,
        'os_cct': None,
        'os_va': None,
        'os_sph': 0.00,
        'os_pr': None,
        'os_fr': None,
        'os_lt': None,
        'os_vt': None,
        'od_al': None,
        'od_ak': None,
        'od_ax': 0.00,
        'od_ad': None,
        'od_add': 0.00,
        'od_bc': None,
        'od_cyl': 0.00,
        'od_cct': None,
        'od_va': None,
        'od_sph': 0.00,
        'od_pr': None,
        'od_fr': None,
        'od_lt': None,
        'od_vt': None,
    }

    # 遍历所有键，尝试从 GET 参数中获取并覆盖
    for key in simple.keys():
        try:
            value = request.GET.get(key)
            if value is not None:
                # 注意：GET 参数都是字符串，可能需要根据目标类型进行转换
                # 原始代码直接赋值字符串，这里保持相同行为（不做类型转换）
                simple[key] = value
        except Exception:
            # 忽略异常，保持默认值
            pass

    return simple