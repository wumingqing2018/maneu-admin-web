from django.shortcuts import render


def index(request):
    return render(request, 'report_index.html')


def insert(request):
    return render(request, 'report_insert.html')


def detail(request):
    return render(request, 'report_detail.html')
