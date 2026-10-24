"""common/util_common.py — 杂项工具"""
import random


def get_random_code():
    """生成 6 位数字验证码字符串（100000~999999）"""
    return str(random.randint(100000, 999999))