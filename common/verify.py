import re
import time
from uuid import UUID

"""
通用校验工具
"""


def is_int(string):
    """_summary_

    Args:
        string (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        re_match = re.match(r"^[0-9]\d*$", string, flags=0)
        if re_match:
            return int(string)
    except BaseException as msg:
        print("error", msg)
    return 0


def order_id_method_get(request):
    """
    检验GET请求的order_id是否为32位正整数
    """
    if request.method == 'GET':
        try:
            order_id = request.GET['order_id']
            if len(order_id) == 36:
                return order_id
        except Exception as msg:
            print(msg)
    return None


def order_id_method_post(request):
    if request.method == 'POST':
        try:
            order_id = request.POST['order_id']
            if len(order_id) == 36:
                return order_id
        except Exception as msg:
            print(msg)
    return None


def order_token_method_get(request):
    if request.method == 'GET':
        try:
            order_token = request.GET['order_token']
            re_match = re.match(r"^\d{32}$", order_token, flags=0)
            if re_match:
                return order_token
        except Exception as msg:
            print(msg)
    return None


def order_token_method_post(request):
    if request.method == 'POST':
        try:
            order_token = request.POST['order_token']
            re_match = re.match(r"^\d{32}$", order_token, flags=0)
            if re_match:
                return order_token
        except Exception as msg:
            print(msg)
    return None


def phone_method_Post(request):
    if request.method == 'POST':
        try:
            phone = request.POST['phone']
            re_match = re.match(r"^\d{11}$", phone, flags=0)
            if re_match:
                return phone
        except Exception as msg:
            print(msg)
    return None


def date_method_post(request):
    """判断是否是一个有效的日期字符串"""
    try:
        str_date = request.POST['content']
        if ":" in str_date:
            time.strptime(str_date, "%Y-%m-%d %H:%M:%S")
        else:
            time.strptime(str_date, "%Y-%m-%d")
        return str_date
    except BaseException as e:
        print(e)
        return None


def verifyUUid(str=''):
    try:
        UUID(str).version
        return True
    except:
        return False
