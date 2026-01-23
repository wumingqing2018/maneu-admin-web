import json


def guest_simple(request):
    simple = {'age': '', 'sex': '', 'dfh': '无', 'ot': '正', 'em': '交替'}

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
        'plan': None,
        'pd': None,
        'os_al': None,
        'os_ak': None,
        'os_ax': 0.00,
        'os_ad': None,
        'os_add': 0.00,
        'os_bc': None,
        'os_cyl': 0.00,
        'os_cct': None,
        'os_va': None,
        'os_sph': 0.00,
        'os_pr': None,
        'os_fr': None,
        'os_lt': None,
        'os_vt': None,
        'od_al': None,
        'od_ak': None,
        'od_ax': 0.00,
        'od_ad': None,
        'od_add': 0.00,
        'od_bc': None,
        'od_cyl': 0.00,
        'od_cct': None,
        'od_va': None,
        'od_sph': 0.00,
        'od_pr': None,
        'od_fr': None,
        'od_lt': None,
        'od_vt': None,
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

    plan = request.GET.get('plan')
    if plan == '两用解决方案' or plan == '远用解决方案' or plan == '近用解决方案' or plan == '':
        simple['plan'] = plan

    return simple
