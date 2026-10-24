// static/javascript/maneu_report/insert20260707.js
// 新增验光报告：数据收集 + 提交

(function () {
    'use strict';

    // ============================================================
    // 工具
    // ============================================================
    function val(id) {
        return ($('#' + id).val() || '').trim();
    }

    function setupToggle(btnId, panelId) {
        var $btn = $('#' + btnId);
        var $panel = $('#' + panelId);
        $btn.on('click', function () {
            $panel.slideToggle(200);
            $btn.find('i').toggleClass('bi-chevron-down bi-chevron-up');
        });
    }

    // ============================================================
    // 数据收集：整理成对象（guest / report.od / report.os）
    // ============================================================
    function collectData() {
        return {
            guest: {
                name:   val('name'),
                phone:  val('phone'),
                remark: val('remark'),
                sex:    val('sex'),
                age:    val('age'),
                ot:     val('ot'),
                em:     val('em'),
                dfh:    val('dfh'),
            },
            report: {
                plan: val('PLAN'),
                pd:   val('PD'),
                od: {
                    va:  val('OD_VA'),
                    sph: val('OD_SPH'),
                    cyl: val('OD_CYL'),
                    ax:  val('OD_AX'),
                    pr:  val('OD_PR'),
                    fr:  val('OD_FR'),
                    al:  val('OD_AL'),
                    ak:  val('OD_AK'),
                    ad:  val('OD_AD'),
                    cct: val('OD_CCT'),
                    lt:  val('OD_LT'),
                    vt:  val('OD_VT'),
                    bc:  val('OD_BC'),
                    add: val('OD_ADD'),
                },
                os: {
                    va:  val('OS_VA'),
                    sph: val('OS_SPH'),
                    cyl: val('OS_CYL'),
                    ax:  val('OS_AX'),
                    pr:  val('OS_PR'),
                    fr:  val('OS_FR'),
                    al:  val('OS_AL'),
                    ak:  val('OS_AK'),
                    ad:  val('OS_AD'),
                    cct: val('OS_CCT'),
                    lt:  val('OS_LT'),
                    vt:  val('OS_VT'),
                    bc:  val('OS_BC'),
                    add: val('OS_ADD'),
                },
            },
        };
    }

    // ============================================================
    // 分组对象 → 扁平（form-urlencoded 兼容）
    // ============================================================
    function flatten(data) {
        var flat = {};

        flat.name   = data.guest.name;
        flat.phone  = data.guest.phone;
        flat.remark = data.guest.remark;
        flat.sex    = data.guest.sex;
        flat.age    = data.guest.age;
        flat.ot     = data.guest.ot;
        flat.em     = data.guest.em;
        flat.dfh    = data.guest.dfh;

        flat.plan = data.report.plan;
        flat.pd   = data.report.pd;

        Object.keys(data.report.od).forEach(function (k) {
            flat['od_' + k] = data.report.od[k];
        });
        Object.keys(data.report.os).forEach(function (k) {
            flat['os_' + k] = data.report.os[k];
        });

        return flat;
    }

    // ============================================================
    // 提交
    // ============================================================
    var isSubmitting = false;

    function submit() {
        if (isSubmitting) return;

        var grouped = collectData();
        var flat = flatten(grouped);

        console.log('[report/insert] grouped =', grouped);
        console.log('[report/insert] flat    =', flat);

        var token = localStorage.getItem('access_token') || '';
        if (!token) {
            alert('请先登录');
            return;
        }

        var $btn = $('#submitReport');
        var originalText = $btn.html();

        isSubmitting = true;
        $btn.prop('disabled', true)
            .html('<span class="spinner-border spinner-border-sm me-1"></span>提交中...');

        $.ajax({
            url: window.REPORT_INSERT_API,           // ← 从 window 读（HTML 里定义的）
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token,
            },
            data: flat,                              // jQuery 自动 form-urlencoded
            dataType: 'json',
            success: function (res) {
                if (res && res.status === true) {
                    alert('提交成功');
                    location.href = window.REPORT_LIST_URL || '/';   // ← 从 window 读
                } else {
                    alert((res && res.message) || '提交失败');
                }
            },
            error: function (xhr) {
                var msg = '网络错误，请稍后重试';
                if (xhr.status === 401) {
                    msg = '登录已过期，请重新登录';
                } else {
                    try {
                        var data = JSON.parse(xhr.responseText);
                        msg = data.message || msg;
                    } catch (e) {}
                }
                alert(msg);
            },
            complete: function () {
                isSubmitting = false;
                $btn.prop('disabled', false).html(originalText);
            },
        });
    }

    // ============================================================
    // 初始化
    // ============================================================
    $(function () {
        setupToggle('toggleGuest', 'guestExtra');
        setupToggle('toggleReport', 'reportExtra');
        $('#submitReport').on('click', submit);
    });

})();