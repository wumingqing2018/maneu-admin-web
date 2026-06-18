from django import forms
from django.core.validators import RegexValidator
from django.forms import widgets
from common.common import get_random_code

class SendSMSForm(forms.Form):
    call = forms.CharField(
        label="手机号",
        required=True,
        strip=True,
        widget=widgets.TextInput(
            attrs={'id': 'call', 'class': 'form-control', 'placeholder': '请输入手机号'}
        ),
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '请输入正确的手机号格式')],
        error_messages={'required': '手机号不能为空'},
    )

    def clean(self):
        cleaned_data = super().clean()
        call = cleaned_data.get('call')
        if not call:
            return cleaned_data
        # 生成6位随机验证码
        code = get_random_code()  # 注意加括号
        # 存入 cleaned_data 供视图使用
        cleaned_data['code'] = code
        # 注意：这里不查询用户，不更新数据库，只生成验证码
        return cleaned_data