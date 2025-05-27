import os, random, time, requests

from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.client import AcsClient
from aliyunsdkdysmsapi.request.v20170525.SendSmsRequest import SendSmsRequest
from pathlib import Path


def get_miniprogram_token():
    APPID = "wxf48b774de9be5613"
    APPSECRET = "e07b22bd5cac3c5a74baf9e03ffc7ce1"
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}"
    return requests.get(url).json()


def get_wxacode(access_token, code="", width=430,):
    path = f"static/images/maneu_order/{code}.png"
    if not Path(path).exists():
        url = f"https://api.weixin.qq.com/wxa/getwxacode?access_token={access_token}"

        params = {
            "path": f"pages/verify/verify?code={code}",  # 小程序页面路径（可带参数）
            "width": width,  # 二维码宽度（单位px）
            "auto_color": False,  # 是否自动配色
            "line_color": {"r": 0, "g": 0, "b": 0},  # 手动指定颜色（RGB）
            "is_hyaline": False  # 是否透明背景
        }

        response = requests.post(url, json=params)

        # 保存为图片文件
        if response.headers['Content-Type'] == 'image/jpeg':
            with open(path, "wb") as f:
                f.write(response.content)
            print(f"小程序码已保存至: {path}")
        else:
            print("生成失败:", response.json())  # 返回错误信息（如参数错误）
    else:
        print(f"1+++小程序码已保存至: {path}")


def current_time():
    """
    返回当前时间
    格式: Y-M-D H:M:S
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def getip(request):
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        return request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        return request.META.get("REMOTE_ADDR")


def sendsms(code, call):
    credentials = AccessKeyCredential(os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'], os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'])

    request = SendSmsRequest()
    request.set_accept_format('json')
    request.set_SignName("徕可")
    request.set_TemplateCode("SMS_471990239")
    request.set_PhoneNumbers(call)
    request.set_TemplateParam({'code': code})

    client = AcsClient(region_id='cn-shenzhen', credential=credentials)
    response = client.do_action_with_exception(request)

    return eval(response)


def get_random_code():
    return random.randint(100000, 999999)


def time_start():
    return time.strftime("%Y-%m-%d 00:00:00", time.localtime())


def time_end():
    return time.strftime("%Y-%m-%d 23:59:59", time.localtime())


def time_time():
    return time.time()