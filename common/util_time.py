"""common/util_time.py — 时间边界工具"""
from django.utils import timezone


def time_now():
    """当前时间（microsecond=0），返回 datetime"""
    return timezone.localtime().replace(microsecond=0)


def time_start():
    """当天 00:00:00，返回 datetime"""
    return timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)


def time_end():
    """当天 23:59:59，返回 datetime"""
    return timezone.localtime().replace(hour=23, minute=59, second=59, microsecond=999999)