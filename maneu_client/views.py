from django.shortcuts import render, HttpResponseRedirect, reverse
from maneu_client import service
import json

def index(request):
    list = service.find_guess_list(user_id=request.session.get('id'))
    if list:
        return render(request, 'maneu_client/index.html', {'orderlist': list})
    else:
        orderlist = service.find_order_all(users_id=request.session.get('id'))  # 查找今日订单
        for order in orderlist:
            print(service.guess_update_userIdandId(user_id=order.users_id, id=order.guess_id))
            print(service.guess_update_subjective_id(subjective_id=order.subjectiverefraction_id, id=order.guess_id))

        list = service.find_guess_list(user_id=request.session.get('id'))
        return render(request, 'maneu_client/index.html', {'orderlist':list})


def detail(request):
    guess = service.find_guess_id(id=request.POST.get('id'))
    users = service.find_users_id(id=request.session.get('id'))
    Subjective = service.find_subjectiverefraction_id(id=guess.subjective_id)
    subjectiverefraction = json.loads(Subjective.content)
    return render(request, 'maneu_client/detail.html', {'guess': guess, 'users': users, 'subjectiverefraction': subjectiverefraction})


def insert(request):
    if request.method == 'POST':
        ManeuSubjectiveRefraction = service.ManeuSubjectiveRefraction_insert(content=request.POST.get('Subjective_refraction'))
        ManeuGuess_id = service.ManeuGuess_insert(content=request.POST.get('Guess_information'),
                                                  subjective_id=ManeuSubjectiveRefraction.id,
                                                  user_id=request.session.get('id'))
        return HttpResponseRedirect(reverse('maneu_client:index'))
    return render(request, 'maneu_client/insert.html')


def search(request):
    return render(request, 'maneu_client/index.html')
