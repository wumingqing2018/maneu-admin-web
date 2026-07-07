import logging
from django import forms
from django.core.cache import cache
from django.core.validators import RegexValidator
from django.forms import widgets

from common.common import get_random_code
from maneu_guest.service import guest_search_call

logger = logging.getLogger(__name__)


class SendSMSForm(forms.Form):
    """短信验证码发送表单"""
    call = forms.CharField(
        label="手机号",
        required=True,
        strip=True,
        widget=widgets.TextInput(
            attrs={
                'id': 'call',
                'class': 'form-control',
                'placeholder': '请输入手机号'
            }
        ),
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '请输入正确的手机号格式')],
        error_messages={'required': '手机号不能为空'},
    )

    def clean_call(self):
        """校验手机号是否存在，并检查发送频率"""
        call = self.cleaned_data['call']

        # 1. 检查是否频繁发送（60秒内同一手机号只允许发一次）
        cache_key = f'sms_limit_{call}'
        if cache.get(cache_key):
            raise forms.ValidationError('发送过于频繁，请60秒后再试')

        # 2. 检查用户是否已注册
        try:
            guest = guest_search_call(call)
        except Exception as e:
            logger.exception('查询用户失败')          # 记录系统异常
            raise forms.ValidationError('系统繁忙，请稍后重试')

        if not guest:
            raise forms.ValidationError('该手机号未注册')

        return call

    def clean(self):
        cleaned_data = super().clean()
        call = cleaned_data.get('call')
        if call:
            cleaned_data['code'] = get_random_code()
        return cleaned_data