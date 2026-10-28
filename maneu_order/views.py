from django.shortcuts import render


def index(request):
    return render(request, 'order_index.html')


def insert(request):
    return render(request, 'order_insert.html')


def detail(request):
    return render(request, 'order_detail.html')
