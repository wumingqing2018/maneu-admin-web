from django import forms
from django.core.validators import RegexValidator
from django.forms import widgets

from maneu_order.service import find_order_phone


class GuessForm(forms.Form):
    phone = forms.CharField(label="账号",
                            required=True,
                            strip=True,
                            widget=widgets.TextInput(
                                attrs={
                                    'id': 'phone', 'class': 'form-control', 'placeholder': '账号'}
                            ),
                            validators=[RegexValidator(
                                r'^[A-Za-z0-9_]+$', '只支持数字和字母')],
                            error_messages={'required': '请输入账号'},
                            )
    code = forms.CharField(label="密码",
                           required=True,
                           strip=True,
                           widget=widgets.PasswordInput(
                               attrs={
                                   'id': 'code', 'class': 'form-control', 'placeholder': '密码'}
                           ),
                           validators=[RegexValidator(
                               r'^[A-Za-z0-9_]+$', '只支持数字和字母')],
                           error_messages={'required': '请输入密码'},
                           )

    def clean(self):
        username = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('code')
        verify = find_order_phone(phone=username)
        if verify == None:
            raise forms.ValidationError('登录失败')
