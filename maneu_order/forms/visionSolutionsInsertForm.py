from django import forms
from django.core.validators import RegexValidator
from django.forms import widgets


class VisionSolutionsInsertForm(forms.Form):
    search = forms.CharField(label="单号",
                             required=True,
                             widget=widgets.TextInput(
                                 attrs={'id': 'search', 'placeholder': '手机号', 'class': 'col-md-9 form-control'}
                             ),
                             validators=[RegexValidator(r'^[0-9]+$', '请输入正确手机号')],
                             error_messages={'request': '请输入手机号'},
                             )

    # VS_remark = request.POST['VS_remark'],
    # OD_BC_DS = request.POST['OD_BC_DS'],
    # OD_BC_CYL = request.POST['OD_BC_CYL'],
    # OD_BC_AX = request.POST['OD_BC_AX'],
    # OD_BC_PR = request.POST['OD_BC_PR'],
    # OD_BC_FR = request.POST['OD_BC_FR'],
    # OD_BC_ADD = request.POST['OD_BC_ADD'],
    # OD_BC_NA = request.POST['OD_BC_NA'],
    # OS_BC_DS = request.POST['OS_BC_DS'],
    # OS_BC_CYL = request.POST['OS_BC_CYL'],
    # OS_BC_AX = request.POST['OS_BC_AX'],
    # OS_BC_PR = request.POST['OS_BC_PR'],
    # OS_BC_FR = request.POST['OS_BC_FR'],
    # OS_BC_ADD = request.POST['OS_BC_ADD'],
    # OS_BC_NA = request.POST['OS_BC_NA']
