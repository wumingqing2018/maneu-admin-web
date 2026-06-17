from django import forms
from django.core.validators import RegexValidator
from django.forms import widgets


class OrderInsertForm(forms.Form):
    c_name = forms.CharField(label='客户姓名',
                             required=True,
                             strip=True,
                             min_length=2,
                             max_length=32,
                             widget=widgets.TextInput(
                                 attrs={'id': 'c_name', 'class': 'form-control', 'placeholder': '客户姓名'}),
                             validators=[RegexValidator(r'^[\u4E00-\u9FA5A-Za-z0-9_]+$', '不能输入特殊字符')],
                             error_messages={'required': '请输入姓名', 'min_length': '格式不正确',
                                             'max_length': '格式不正确'},
                             )
    c_phone = forms.CharField(label='客户电话',
                              required=True,
                              strip=True,
                              min_length=11,
                              max_length=11,
                              widget=widgets.TextInput(
                                  attrs={'id': 'c_phone', 'class': 'form-control', 'placeholder': '客户电话'}),
                              validators=[RegexValidator(r'1[1-9][0-9]{9}', '手机号格式不正确')],
                              error_messages={'required': '请输入电话'},
                              )
    order = forms.CharField(label="订单",
                            required=False,
                            strip=True,
                            )
    remark = forms.CharField(label="备注",
                             required=False,
                             strip=True,
                             max_length=2048,
                             # validators=[RegexValidator(r'^[\u4E00-\u9FA5A-Za-z0-9_]+$', '不能输入特殊字符')],
                             )
