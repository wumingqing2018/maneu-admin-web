import os
import random
import secrets
import time
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, Union

import requests
from django.http import HttpRequest  # 用于 getip 的类型提示
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.client import AcsClient
from aliyunsdkdysmsapi.request.v20170525.SendSmsRequest import SendSmsRequest


# ======================= 常量定义 =======================
# 微信小程序配置（生产环境应从环境变量或配置文件读取）
WECHAT_APPID = "wxf48b774de9be5613"
WECHAT_APPSECRET = "e07b22bd5cac3c5a74baf9e03ffc7ce1"

# 阿里云短信配置（从环境变量读取）
ALIBABA_CLOUD_ACCESS_KEY_ID = os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID')
ALIBABA_CLOUD_ACCESS_KEY_SECRET = os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
if not ALIBABA_CLOUD_ACCESS_KEY_ID or not ALIBABA_CLOUD_ACCESS_KEY_SECRET:
    raise RuntimeError("请设置环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET")

# 阿里云短信固定参数
SMS_SIGN_NAME = "爱视光学"
SMS_TEMPLATE_CODE = "SMS_485420526"
SMS_REGION_ID = 'cn-shenzhen'

# 小程序码保存目录
QR_CODE_DIR = Path("static/images/maneu_order")
QR_CODE_DIR.mkdir(parents=True, exist_ok=True)  # 自动创建目录


# ======================= 工具函数 =======================

def generate_random_32hex() -> str:
    """
    生成32位随机十六进制字符串，使用 secrets 模块保证安全性。

    Returns:
        str: 32位十六进制字符串（16字节）。
    """
    return secrets.token_hex(16)  # 16字节 = 32位十六进制


def get_miniprogram_token() -> Dict[str, Any]:
    """
    获取微信小程序全局接口调用凭证（access_token）。

    注意：access_token 有效期为 2 小时，建议生产环境缓存复用。

    Returns:
        dict: 微信 API 返回的 JSON 数据，通常包含 'access_token' 和 'expires_in'。
               若失败则包含 'errcode' 和 'errmsg'。
    """
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_APPID}&secret={WECHAT_APPSECRET}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"errcode": -1, "errmsg": f"网络请求失败: {str(e)}"}


def get_wxacode(access_token: str, code: str = "", width: int = 430) -> Dict[str, Any]:
    """
    获取微信小程序码（无限制二维码），并保存为本地图片文件。

    Args:
        access_token: 微信小程序 access_token。
        code: 自定义场景值（最多32个字符），会作为参数 scene 传给小程序。
        width: 二维码宽度（像素），范围 280~1280，默认 430。

    Returns:
        dict: 包含 'code'（状态码）和 'messages'（描述信息）的字典。
               - 200: 生成成功
               - 502: 文件已存在
               - 501: 生成失败（具体错误信息在 messages 中）
    """
    # 确保 scene 不超过 32 位（微信限制）
    scene = code[:32] if len(code) > 32 else code
    file_path = QR_CODE_DIR / f"{code}.png"

    if file_path.exists():
        return {'code': 502, 'messages': f"小程序码已存在: {file_path}"}

    url = "https://api.weixin.qq.com/wxa/getwxacodeunlimit"
    params = {
        "scene": scene,
        "page": "pages/verify/verify",      # 小程序页面路径
        "check_path": True,
        "env_version": "trial",             # 体验版（生产环境可改为 "release"）
        "width": width,
        "auto_color": False,
        "line_color": {"r": 0, "g": 0, "b": 0},
        "is_hyaline": False
    }

    try:
        response = requests.post(
            f"{url}?access_token={access_token}",
            json=params,
            timeout=30
        )
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', '')

        if content_type == 'image/jpeg':
            with open(file_path, "wb") as f:
                f.write(response.content)
            return {'code': 200, 'messages': f"小程序码已保存至: {file_path}"}
        else:
            error_info = response.json()
            return {'code': 501, 'messages': f"生成失败: {error_info}"}
    except requests.RequestException as e:
        return {'code': 501, 'messages': f"网络请求异常: {str(e)}"}
    except Exception as e:
        return {'code': 501, 'messages': f"未知错误: {str(e)}"}


def current_time() -> str:
    """
    返回当前时间的格式化字符串。

    Returns:
        str: 格式为 "YYYY-MM-DD HH:MM:SS" 的当前时间。
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def getip(request: HttpRequest) -> str:
    """
    从 Django 请求对象中获取客户端真实 IP 地址。
    优先获取 HTTP_X_FORWARDED_FOR（代理/负载均衡场景），否则取 REMOTE_ADDR。

    Args:
        request: Django HttpRequest 对象。

    Returns:
        str: 客户端 IP 地址。
    """
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        # 如果有多个代理，第一个 IP 是真实客户端 IP
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def sendsms(code: int, phone_number: str) -> Dict[str, Any]:
    """
    通过阿里云短信服务发送验证码。

    Args:
        code: 6 位数字验证码。
        phone_number: 接收短信的手机号码。

    Returns:
        dict: 阿里云 API 返回的响应字典（已转为 Python 对象）。
              常见字段: 'Code'（OK 表示成功）、'Message'、'RequestId'。
    """
    credentials = AccessKeyCredential(ALIBABA_CLOUD_ACCESS_KEY_ID,
                                      ALIBABA_CLOUD_ACCESS_KEY_SECRET)
    client = AcsClient(region_id=SMS_REGION_ID, credential=credentials)

    request = SendSmsRequest()
    request.set_accept_format('json')
    request.set_SignName(SMS_SIGN_NAME)
    request.set_TemplateCode(SMS_TEMPLATE_CODE)
    request.set_PhoneNumbers(phone_number)
    request.set_TemplateParam({'code': str(code)})

    try:
        response = client.do_action_with_exception(request)
        # 响应为 bytes，需解码为字符串并转为字典
        return eval(response.decode('utf-8'))
    except Exception as e:
        return {'Code': 'Error', 'Message': str(e)}


def get_random_code() -> int:
    """
    生成 6 位随机数字验证码（100000 ~ 999999）。

    Returns:
        int: 6 位随机整数。
    """
    return random.randint(100000, 999999)


def time_start() -> str:
    """
    获取当天开始时间（00:00:00）。

    Returns:
        str: 格式为 "YYYY-MM-DD 00:00:00" 的字符串。
    """
    return time.strftime("%Y-%m-%d 00:00:00", time.localtime())


def time_end() -> str:
    """
    获取当天结束时间（23:59:59）。

    Returns:
        str: 格式为 "YYYY-MM-DD 23:59:59" 的字符串。
    """
    return time.strftime("%Y-%m-%d 23:59:59", time.localtime())


def get_phone_number(code: str, access_token: str) -> Dict[str, Union[bool, str]]:
    """
    通过微信小程序前端获取的 code，换取用户手机号。

    Args:
        code: 小程序端调用 wx.login 后获取的临时凭证（或手机号授权 code）。
        access_token: 微信小程序接口调用凭证。

    Returns:
        dict: 包含 'status'（布尔值，True 表示成功）和 'message'（手机号或错误描述）。
              成功时 message 为手机号字符串。
    """
    url = f"https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token={access_token}"
    payload = {"code": code}

    try:
        resp = requests.post(url, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        return {'status': False, 'message': f"网络请求失败: {str(e)}"}

    if data.get('errcode') == 0:
        phone_info = data.get('phone_info', {})
        phone_number = phone_info.get('phoneNumber', '')
        return {'status': True, 'message': phone_number}
    else:
        errmsg = data.get('errmsg', '未知错误')
        return {'status': False, 'message': errmsg}