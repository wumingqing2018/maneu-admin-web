from django.http import JsonResponse

from common import common
from maneu_index import service


# Create your views here.

def index(request):
    time_list = common.getEveryDay(begin_date=request.GET['start_day'], end_date=request.GET['end_day'])
    content_list = service.ManeuOrder_index(admin_id=request.session.get('id'), start=request.GET['start'], end=request.GET['end'])
    time_newList = []
    content_newList = []
    for a in content_list:
        content_newList.append(str(a.time.date()))
    for b in time_list:
        time_newList.append(content_newList.count(b))
    return JsonResponse({'time_list': time_list, 'time_newList': time_newList, 'count': content_list.count()})