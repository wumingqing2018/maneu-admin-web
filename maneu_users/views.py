from django.shortcuts import HttpResponseRedirect, reverse
from django.shortcuts import render

from common import verify
from maneu_users import serivce


def user_detail(request):
    user_id = request.session.get('id')
    if user_id:
        return render(request, 'maneu_users/user_detail.html', {'user': serivce.find_user(user_id)})
    else:
        return render(request, 'maneu/error.html', {'msg': "请求出错"})


def user_insert(request):
    if request.method == 'POST':
        if request.POST['gift_password'] == '214772680':
            updata = serivce.user_insert(username=request.POST['username'],
                                         nickname=request.POST['nickname'], password=request.POST['password'],
                                         phone=request.POST['phone'], email=request.POST['email'],
                                         remark=request.POST['remark'])
            return HttpResponseRedirect(reverse('login'))
    return render(request, 'maneu_users/user_insert.html')


def user_updata(request):
    user_id = request.session.get('id')
    msg = ''
    if request.method == 'POST':
        updata = serivce.user_update(old_password=request.POST['old_password'], user_id=user_id,
                                     nickname=request.POST['nickname'], password=request.POST['password'],
                                     phone=request.POST['phone'], email=request.POST['email'],
                                     remark=request.POST['remark'])
        print(updata)
        if updata:
            msg = '密码验证错误，请在密码验证输入正确的登录密码'
        else:
            return HttpResponseRedirect(reverse('maneu_users:user_detail'))
    user = serivce.find_user(user_id)
    return render(request, 'maneu_users/user_updata.html', {'user': user, 'msg': msg})
