from django.shortcuts import render


def index(request):
    return render(request, 'maneu/index.html')


def login(request):
    return render(request, 'maneu/login.html')
