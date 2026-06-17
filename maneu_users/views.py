from django.shortcuts import HttpResponseRedirect, reverse
from django.shortcuts import render

from maneu_users import serivce


def user_list(request):
    return render(request, 'maneu_users/index.html', {'user_list': serivce.find_user_all()})


def user_detail(request):
    admin_id = request.session.get('id')
    if admin_id:
        return render(request, 'maneu_users/detail.html', {'maneu_users': serivce.find_user(admin_id)})
    else:
        return HttpResponseRedirect(reverse('index'))


def user_insert(request):
    if request.method == 'POST':
        if request.POST['gift_password'] == '214772680':
            updata = serivce.user_insert(username=request.POST['username'],
                                         nickname=request.POST['nickname'], password=request.POST['password'],
                                         phone=request.POST['phone'], email=request.POST['email'],
                                         remark=request.POST['remark'])
            return HttpResponseRedirect(reverse('login'))
    return render(request, 'maneu_users/insert.html')


def user_updata(request):
    admin_id = request.session.get('id')
    msg = ''
    if request.method == 'POST':
        updata = serivce.user_update(old_password=request.POST['old_password'], admin_id=admin_id,
                                     localtion=request.POST.get('localtion'),
                                     nickname=request.POST['nickname'], password=request.POST['password'],
                                     phone=request.POST['phone'], email=request.POST['email'],
                                     remark=request.POST['remark'])
        if updata:
            msg = '密码验证错误，请在密码验证输入正确的登录密码'
        else:
            return HttpResponseRedirect(reverse('maneu_users:user_detail'))
    user = serivce.find_user(admin_id)
    return render(request, 'maneu_users/updata.html', {'maneu_users': user, 'msg': msg})
