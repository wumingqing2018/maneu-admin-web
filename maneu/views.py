from django.shortcuts import render
from maneu.models import ManeuReport
import json

def index(request):
    reportList = ManeuReport.objects.filter().all()
    for report in reportList:
        content = {
            "plan": report.plan,
            "sex": report.sex,
            "age": report.age,

            "dfh": report.dfh,
            "ot": report.ot,
            "em": report.em,
            "pd": report.pd,

            "od": {
                "al": report.od_al,
                "ak": report.od_ak,
                "ax": report.od_ax,
                "ad": report.od_ad,
                "add": report.od_add,
                "bc": report.od_bc,
                "cyl": report.od_cyl,
                "cct": report.od_cct,
                "va": report.od_va,
                "sph": report.od_sph,
                "pr": report.od_pr,
                "fr": report.od_fr,
                "lt": report.od_lt,
                "vt": report.od_vt,
            },
            "os": {
                "al": report.os_al,
                "ak": report.os_ak,
                "ax": report.os_ax,
                "ad": report.os_ad,
                "add": report.os_add,
                "bc": report.os_bc,
                "cyl": report.os_cyl,
                "cct": report.os_cct,
                "va": report.os_va,
                "sph": report.os_sph,
                "pr": report.os_pr,
                "fr": report.os_fr,
                "lt": report.os_lt,
                "vt": report.os_vt,
            },
        }
        print(ManeuReport.objects.filter(id=report.id).update(content=json.dumps(content)))
    return render(request, 'maneu/index.html')


def login(request):
    return render(request, 'maneu/login.html')
