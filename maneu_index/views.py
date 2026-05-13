import json

from django.shortcuts import render

from maneu.models import ManeuReport

from common.verify import is_uuid


def is_float(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def clean_numeric(queryset, field_name):
    """从查询集中提取指定字段的有效 float 列表"""
    result = []
    for obj in queryset:
        val = getattr(obj, field_name, None)
        if val and is_float(val):
            result.append(float(val))
    return result


def frequency_dict(data_list, bins=None, bin_width=0.5):
    """将数据转换为频数分布字典，用于柱状图"""
    if not data_list:
        return {}, []
    if bins is None:
        min_val = min(data_list)
        max_val = max(data_list)
        # 自定义分箱
        pass
    # 这里简单返回原始列表，让 ECharts 自动处理，或者在前端统计
    return data_list  # 前端用 echarts 直方图


def index(request):
    admin_id = is_uuid(request.session.get('id'))
    if admin_id:
        # 获取全部验光记录（实际生产环境需考虑数据量，可加分页或日期过滤）
        reports = ManeuReport.objects.filter(admin_id=admin_id).all()

        # 1. 视力数据 (暂当分类数据处理，假设 VA 是小数视力或对数视力)
        od_va = clean_numeric(reports, 'od_va')
        os_va = clean_numeric(reports, 'os_va')

        # 视力分级统计（按 ≤0.1, 0.2-0.5, 0.6-1.0, >1.0 简单示范）
        def va_category(values):
            cat = {'<=0.1': 0, '0.2-0.5': 0, '0.6-1.0': 0, '>1.0': 0}
            for v in values:
                if v <= 0.1:
                    cat['<=0.1'] += 1
                elif v <= 0.5:
                    cat['0.2-0.5'] += 1
                elif v <= 1.0:
                    cat['0.6-1.0'] += 1
                else:
                    cat['>1.0'] += 1
            return cat

        od_va_cat = va_category(od_va)
        os_va_cat = va_category(os_va)

        # 2. 球镜
        od_sph = clean_numeric(reports, 'od_sph')
        os_sph = clean_numeric(reports, 'os_sph')

        # 3. 柱镜
        od_cyl = clean_numeric(reports, 'od_cyl')
        os_cyl = clean_numeric(reports, 'os_cyl')

        # 4. 轴位（极坐标需要角度数据，0-180）
        od_ax = clean_numeric(reports, 'od_ax')
        os_ax = clean_numeric(reports, 'os_ax')

        # 5. 眼轴长度
        od_al = clean_numeric(reports, 'od_al')
        os_al = clean_numeric(reports, 'os_al')

        # 6. 角膜曲率
        od_ak = clean_numeric(reports, 'od_ak')
        os_ak = clean_numeric(reports, 'os_ak')

        # 7. ADD
        od_add = clean_numeric(reports, 'od_add')
        os_add = clean_numeric(reports, 'os_add')

        context = {
            'od_va_cat': json.dumps(od_va_cat),
            'os_va_cat': json.dumps(os_va_cat),
            'od_sph': json.dumps(od_sph),
            'os_sph': json.dumps(os_sph),
            'od_cyl': json.dumps(od_cyl),
            'os_cyl': json.dumps(os_cyl),
            'od_ax': json.dumps(od_ax),
            'os_ax': json.dumps(os_ax),
            'od_al': json.dumps(od_al),
            'os_al': json.dumps(os_al),
            'od_ak': json.dumps(od_ak),
            'os_ak': json.dumps(os_ak),
            'od_add': json.dumps(od_add),
            'os_add': json.dumps(os_add),
        }
    else:
        context = {}
    return render(request, 'index_index.html', context)
