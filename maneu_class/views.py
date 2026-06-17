from django.shortcuts import render, reverse, redirect

from maneu_class import service


def index(request):
    class_List = service.class_list(admin_id=request.session.get('id'))
    return render(request, 'maneu_class/index.html', {'classList': class_List})


def class_insert(request):
    if request.method == 'POST':
        class_insert = service.class_insert(admin_id=request.session.get('id'),
                                            name=request.POST.get('name'),
                                            series=request.POST.get('series'),
                                            color=request.POST.get('color'),
                                            price=request.POST.get('price'))
        return redirect(reverse('maneu_class:class_list'))
    return render(request, 'maneu_class/insert.html')


def class_delete(request):
    if request.method == 'POST':
        class_insert = service.class_delete(admin_id=request.session.get('id'), id=request.POST.get('id'))
        return redirect(reverse('maneu_class:class_list'))
    return render(request, 'maneu_class/insert.html')
