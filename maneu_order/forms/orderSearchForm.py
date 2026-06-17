from django import forms
from django.core.validators import RegexValidator
from django.forms import widgets


class OrderSearchForm(forms.Form):
    search = forms.CharField(label="单号",
                             required=True,
                             widget=widgets.TextInput(
                                 attrs={'id': 'search', 'placeholder': '手机号', 'class': 'col-md-9 form-control'}
                             ),
                             validators=[RegexValidator(r'^[0-9]+$', '请输入正确手机号')],
                             error_messages={'request': '请输入手机号'},
                             )
