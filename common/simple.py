import json

from common.common import current_time


def guest_simple(request):
    simple = {'remark': '', 'time': current_time(), 'name': '', 'call': '', 'age': '', 'sex': '', 'dfh': '无',
              'ot': '正', 'em': '左'}

    for i in list(simple):
        try:
            if request.GET.get(i): simple[i] = request.GET.get(i)
        except:
            pass

    return simple


def order_simple(request_dict):
    simple = {'arg10': '', 'arg11': '', 'arg12': '', 'arg13': '', 'arg14': ''}
    data = []

    try:
        request = json.loads(request_dict)
        for i in request:
            if i != simple: data.append(i)
    except:
        pass

    return json.dumps(data)


def report_simple(request):
    simple = {
        'plan': '远用解决方案',
        'pd': '',
        'os_al': '',
        'os_ak': '',
        'os_ax': '',
        'os_ad': '',
        'os_add': '',
        'os_bc': '',
        'os_cyl': '',
        'os_cct': '',
        'os_va': '',
        'os_sph': '',
        'os_pr': '',
        'os_fr': '',
        'os_lt': '',
        'os_vt': '',
        'od_al': '',
        'od_ak': '',
        'od_ax': '',
        'od_ad': '',
        'od_add': '',
        'od_bc': '',
        'od_cyl': '',
        'od_cct': '',
        'od_va': '',
        'od_sph': '',
        'od_pr': '',
        'od_fr': '',
        'od_lt': '',
        'od_vt': '',
    }

    for i in list(simple):
        try:
            simple[i] = format(float(request.GET.get(i)), '.2f')
        except:
            pass

    od_fr = request.GET.get('od_fr')
    if od_fr == 'BU' or od_fr == 'BD' or od_fr == od_fr == 'BO' or od_fr == 'BI':
        simple['od_fr'] = od_fr

    os_fr = request.GET.get('os_fr')
    if os_fr == 'BU' or os_fr == 'BD' or os_fr == os_fr == 'BO' or os_fr == 'BI':
        simple['os_fr'] = os_fr

    # plan = request.GET.get('plan')
    # if plan == '两用解决方案' or plan == '远用解决方案' or plan == '近用解决方案' or plan == '':
    #     simple['plan'] = plan

    return simple
