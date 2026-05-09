from django.shortcuts import render


def index(request):
    return render(request, 'admin_index.html', {'index_id': request.session.get('id')})


def insert(request):
    return render(request, 'admin_insert.html', {'id': request.session.get('id')})


def update(request):
    return render(request, 'admin_insert.html', {'id': request.session.get('id')})
