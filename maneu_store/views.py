from django.shortcuts import render


def index(request):
    return render(request, 'store_index.html')


def insert(request):
    return render(request, 'store_insert.html')


def detail(request):
    return render(request, 'store_detail.html')
