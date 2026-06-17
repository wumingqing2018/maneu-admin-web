from django import forms
from django.core.validators import RegexValidator


class BatchInsertForm(forms.Form):
    c_name = forms.CharField(label='姓名',
                             required=True,
                             strip=True,
                             min_length=2,
                             max_length=32,
                             validators=[RegexValidator(
                                 r'^[\u4E00-\u9FA5A-Za-z0-9_]+$', '不能输入特殊字符')],
                             error_messages={
                                 'required': '请输入姓名', 'min_length': '姓名信息不能少于2个字符',
                                 'max_length': '产品信息不能超过32个字符'},
                             )
    c_phone = forms.CharField(label='电话',
                              required=True,
                              strip=True,
                              min_length=2,
                              max_length=11,
                              validators=[RegexValidator(
                                  r'^[\u4E00-\u9FA5A-Za-z0-9_]+$', '不能输入特殊字符')],
                              error_messages={
                                  'required': '请输入电话', 'min_length': '电话信息不能少于2个字符',
                                  'max_length': '产品信息不能超过11个字符'},
                              )
    remark = forms.CharField(label="备注",
                             required=True,
                             strip=True,
                             max_length=2048,
                             error_messages={
                                 'required': '请输入产品', 'min_length': '产品信息不能少于2个字符',
                                 'max_length': '产品信息不能超过2048个字符'},
                             )
