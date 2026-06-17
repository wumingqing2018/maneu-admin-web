from django import forms
from django.core.validators import RegexValidator
from django.forms import widgets


class JoinForm(forms.Form):
    username = forms.CharField(label="账号",
                               required=True,
                               strip=True,
                               min_length='8',
                               max_length='128',
                               widget=widgets.TextInput(
                                   attrs={'class': 'form_username', 'placeholder': '账号'}
                               ),
                               validators=[RegexValidator(r'^[A-Za-z0-9_]+$', '只允许输入数字和字母')],
                               error_messages={'required': "请输入账号",
                                               'min_length': "账号长度不能少于8位",
                                               'max_length': "账号长度不能超过128位"},
                               )

    password = forms.CharField(label="密码",
                               required=True,
                               strip=True,
                               min_length='8',
                               max_length='128',
                               widget=widgets.TextInput(
                                   attrs={'class': 'form_password', 'placeholder': '密码'}
                               ),
                               validators=[RegexValidator(r'^[A-Za-z0-9_]+$', '只允许输入数字和字母')],
                               error_messages={'required': "请输入密码",
                                               'min_length': "密码长度不能少于8位",
                                               'max_length': "密码长度不能超过128位"},
                               )

    nickname = forms.CharField(label='店名',
                               required=True,
                               strip=True,
                               widget=widgets.TextInput(
                                   attrs={'class': 'form_nickname', 'placeholder': '店名'}
                               ),
                               validators=[RegexValidator(r'^[\u4e00-\u9fa5]+$', '只支持输入中文')],
                               error_messages={'request': '请输入店名'}
                               )

    phone = forms.CharField(label='手机',
                            required=True,
                            strip=True,
                            widget=widgets.TextInput(
                                attrs={'class': 'form_phone', 'placeholder': '手机'}
                            ),
                            validators=[RegexValidator(r'^[0-9]*$', '号码格式不正确')],
                            error_messages={'request': '请输入号码'})
