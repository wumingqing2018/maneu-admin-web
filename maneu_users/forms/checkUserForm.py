from django import forms
from django.core.validators import RegexValidator
from django.forms import widgets


class CheckUserForm(forms.Form):
    user_id = forms.CharField(required=True,
                              strip=True,
                              widget=widgets.TextInput(attrs={'id': 'user_id'}),
                              validators=[RegexValidator(r'^[0-9]*$', '请输入正确单号')],
                              error_messages={'request': '请输入单号'}
                              )
