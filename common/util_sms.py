"""common/util_sms.py — 阿里云短信发送"""
import json
import os
import logging

from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.client import AcsClient
from aliyunsdkdysmsapi.request.v20170525.SendSmsRequest import SendSmsRequest

logger = logging.getLogger(__name__)

SMS_REGION_ID     = 'cn-shenzhen'
SMS_SIGN_NAME     = '爱视光学'
SMS_TEMPLATE_CODE = 'SMS_485420526'


def send_sms(call, code):
    """调用阿里云短信接口，返回 dict（'Code' == 'OK' 表示成功）"""
    try:
        credentials = AccessKeyCredential(
            os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
            os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
        )
        request = SendSmsRequest()
        request.set_accept_format('json')
        request.set_SignName(SMS_SIGN_NAME)
        request.set_TemplateCode(SMS_TEMPLATE_CODE)
        request.set_PhoneNumbers(call)
        request.set_TemplateParam({'code': str(code)})

        client = AcsClient(region_id=SMS_REGION_ID, credential=credentials)
        response = client.do_action_with_exception(request)
        return json.loads(response.decode('utf-8'))

    except (ClientException, ServerException):
        logger.exception('阿里云 SDK 异常 call=%s', call)
        return {'Code': 'SDK_ERROR', 'Message': 'SDK 调用失败'}
    except Exception:
        logger.exception('短信发送未知异常 call=%s', call)
        return {'Code': 'UNKNOWN_ERROR', 'Message': '发送失败'}