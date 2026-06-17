from django.shortcuts import HttpResponseRedirect, reverse, render

from common import common
from maneu import service
from maneu.forms.loginForm import LoginForm


def index(request):
    """
    首页
    """
    return render(request, 'maneu/index.html')


def login(request):
    """
    登录模块
    获取session key并根据sessionkey 判断用户是否已经登录
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_content = service.find_user_username(username=request.POST['username'])
            request.session['ip'] = common.get_ip(request)
            request.session['id'] = user_content.id
            request.session['nickname'] = user_content.nickname
            return HttpResponseRedirect(reverse('maneu_order:index'))
    return render(request, 'maneu/login.html', {'form': LoginForm()})
