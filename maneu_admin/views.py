from django.shortcuts import render

from maneu_admin import service


def index(request):
    return render(request, 'maneu_admin/index.html', {'id': request.session.get('id')})


def user_insert(request):
    if request.method == 'POST':
        if request.POST['gift_password'] == '214772680':
            updata = service.user_insert(username=request.POST['username'],
                                         nickname=request.POST['nickname'],
                                         password=request.POST['password'],
                                         phone=request.POST['phone'],
                                         email=request.POST['email'])
    return render(request, 'maneu_admin/insert.html')
