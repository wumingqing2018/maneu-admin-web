import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from common.verify import is_uuid
from maneu.models import ManeuReport
from common.jwt_util import _get_admin_id


def _safe_float(val):
    """将字符串或数字安全转换为float，失败返回None"""
    if val is None:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def search_time(request):
    """
    按时间范围查询订单列表（接口）
    GET参数: timeS, timeE   ISO格式本地时间字符串
    返回: {
        "status": bool,
        "message": str,
        "content": [{"id":, "name":, "phone":, "time":, "remark":}, ...]
    }
    """
    admin_id = _get_admin_id(request)
    if not admin_id:
        return JsonResponse({'status': False, 'message': '认证失败，请重新登录', 'content': []})

    timeS = request.POST.get('timeS')
    timeE = request.POST.get('timeE')
    if not timeS or not timeE:
        return JsonResponse({'status': False, 'message': '缺少时间范围参数', 'content': []})

    try:
        # 只查询必要字段，使用 only 减少数据库负载
        queryset = ManeuReport.objects.filter(
            admin_id=admin_id,
            time__range=[timeS, timeE]
        ).only('id', 'name', 'phone', 'time', 'remark').order_by('-time')

        # values 直接返回字典列表，比序列化模型对象更高效
        content = list(queryset.values('id', 'name', 'phone', 'time', 'remark'))
        return JsonResponse({'status': True, 'message': '', 'content': content})
    except Exception as e:
        return JsonResponse({'status': False, 'message': f'服务器错误: {str(e)}', 'content': []})


def search_data(request):
    """
    根据客户姓名或手机号模糊搜索订单（接口）
    GET参数: value  搜索关键词
    返回结构同 search_time
    """
    admin_id = _get_admin_id(request)
    if not admin_id:
        return JsonResponse({'status': False, 'message': '认证失败，请重新登录', 'content': []})

    keyword = request.POST.get('value', '').strip()
    if not keyword:
        return JsonResponse({'status': False, 'message': '搜索关键词不能为空', 'content': []})

    try:
        queryset = ManeuReport.objects.filter(
            admin_id=admin_id
        ).filter(
            # 姓名或手机号包含关键词（不区分大小写）
            name__icontains=keyword
        ) | ManeuReport.objects.filter(
            admin_id=admin_id,
            phone__icontains=keyword
        )

        queryset = queryset.only('id', 'name', 'phone', 'time', 'remark').order_by('-time')
        content = list(queryset.values('id', 'name', 'phone', 'time', 'remark'))
        return JsonResponse({'status': True, 'message': '', 'content': content})
    except Exception as e:
        return JsonResponse({'status': False, 'message': f'服务器错误: {str(e)}', 'content': []})


def statistics(request):
    """
    生成验光数据统计（纯接口，供ECharts前端调用）
    返回JSON包含所有图表所需数据：视力分布、球镜柱镜列表、眼轴长度列表等
    """
    admin_id = _get_admin_id(request)
    if not admin_id:
        return JsonResponse({'status': False, 'message': '认证失败', 'data': {}})

    # 只查询需要做统计的字段，使用 only 大幅减少内存消耗
    reports = ManeuReport.objects.filter(admin_id=admin_id).only(
        'od_va', 'os_va',
        'od_sph', 'os_sph',
        'od_cyl', 'os_cyl',
        'od_al', 'os_al',
        'od_ak', 'os_ak'
    )

    # 初始化存放有效数值的列表
    od_sph, os_sph = [], []
    od_cyl, os_cyl = [], []
    od_al, os_al = [], []
    od_ak, os_ak = [], []

    # 视力分类计数器（左右眼独立）
    va_cat_right = {'<=0.1': 0, '0.2-0.5': 0, '0.6-1.0': 0, '>1.0': 0}
    va_cat_left = {'<=0.1': 0, '0.2-0.5': 0, '0.6-1.0': 0, '>1.0': 0}

    # 一次遍历完成所有字段提取和视力分类
    for report in reports:
        # 右眼视力
        r_va = _safe_float(report.od_va)
        if r_va is not None:
            if r_va <= 0.1:
                va_cat_right['<=0.1'] += 1
            elif r_va <= 0.5:
                va_cat_right['0.2-0.5'] += 1
            elif r_va <= 1.0:
                va_cat_right['0.6-1.0'] += 1
            else:
                va_cat_right['>1.0'] += 1

        # 左眼视力
        l_va = _safe_float(report.os_va)
        if l_va is not None:
            if l_va <= 0.1:
                va_cat_left['<=0.1'] += 1
            elif l_va <= 0.5:
                va_cat_left['0.2-0.5'] += 1
            elif l_va <= 1.0:
                va_cat_left['0.6-1.0'] += 1
            else:
                va_cat_left['>1.0'] += 1

        # 球镜
        sph_r = _safe_float(report.od_sph)
        if sph_r is not None:
            od_sph.append(sph_r)
        sph_l = _safe_float(report.os_sph)
        if sph_l is not None:
            os_sph.append(sph_l)

        # 柱镜
        cyl_r = _safe_float(report.od_cyl)
        if cyl_r is not None:
            od_cyl.append(cyl_r)
        cyl_l = _safe_float(report.os_cyl)
        if cyl_l is not None:
            os_cyl.append(cyl_l)

        # 眼轴长度
        al_r = _safe_float(report.od_al)
        if al_r is not None:
            od_al.append(al_r)
        al_l = _safe_float(report.os_al)
        if al_l is not None:
            os_al.append(al_l)

        # 角膜曲率
        ak_r = _safe_float(report.od_ak)
        if ak_r is not None:
            od_ak.append(ak_r)
        ak_l = _safe_float(report.os_ak)
        if ak_l is not None:
            os_ak.append(ak_l)

    # 构造返回数据，保持与前端的 ECharts 模板一致
    context = {
        'od_va_cat': json.dumps(va_cat_right),
        'os_va_cat': json.dumps(va_cat_left),
        'od_sph': json.dumps(od_sph),
        'os_sph': json.dumps(os_sph),
        'od_cyl': json.dumps(od_cyl),
        'os_cyl': json.dumps(os_cyl),
        'od_al': json.dumps(od_al),
        'os_al': json.dumps(os_al),
        'od_ak': json.dumps(od_ak),
        'os_ak': json.dumps(os_ak),
    }
    return JsonResponse({'status': True, 'message': '', 'data': context})