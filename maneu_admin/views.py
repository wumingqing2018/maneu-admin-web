from django.shortcuts import render


def index(request):
    return render(request, 'maneu_admin/index.html', {'index_id': request.session.get('id')})


def insert(request):
    return render(request, 'maneu_admin/insert.html', {'id': request.session.get('id')})


def update(request):
    return render(request, 'maneu_admin/insert.html', {'id': request.session.get('id')})
