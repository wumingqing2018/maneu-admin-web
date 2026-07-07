
// 通用错误提示（风格与订单管理页保持一致）
function showError(message) {
    alert(message || '操作失败，请稍后重试');
}

// ==================== 防重复提交控制 ====================
let isSubmitting = false;

function setSubmitting(btn, state, originalText = null) {
    isSubmitting = state;
    if (btn) {
        if (state) {
            btn.prop('disabled', true);
            btn.data('original-text', btn.html());
            btn.html('<span class="spinner-border spinner-border-sm me-1" role="status"></span> 提交中...');
        } else {
            btn.prop('disabled', false);
            if (btn.data('original-text')) {
                btn.html(btn.data('original-text'));
            }
        }
    }
}

// ==================== 表单验证 ====================
function validateForm() {
    const name = $('#name').val().trim();
    const phone = $('#phone').val().trim();

    if (!name) {
        showError('请填写客户姓名');
        $('#name').focus();
        return false;
    }
    if (!phone) {
        showError('请填写联系电话');
        $('#phone').focus();
        return false;
    }
    // 简单手机号验证（可根据需要调整）
    const phoneRegex = /^1[3-9]\d{9}$|^\d{7,15}$/;
    if (!phoneRegex.test(phone)) {
        showError('请输入有效的联系电话');
        $('#phone').focus();
        return false;
    }
    return true;
}

// ==================== 提交报告（带防抖与加载状态） ====================
function submitReport() {
    // 防重复提交
    if (isSubmitting) return;

    // 表单验证
    if (!validateForm()) return;

    // 收集所有表单数据
    const formData = {
        time: $('#time').val(),
        name: $('#name').val().trim(),
        phone: $('#phone').val().trim(),
        remark: $('#remark').val().trim(),
        age: $('#age').val().trim(),
        sex: $('#sex').val().trim(),
        dfh: $('#dfh').val().trim(),
        ot: $('#ot').val().trim(),
        em: $('#em').val().trim(),
        plan: $('#PLAN').val(),
        pd: $('#PD').val(),
        od_va: $('#OD_VA').val(),
        od_sph: $('#OD_SPH').val(),
        od_cyl: $('#OD_CYL').val(),
        od_ax: $('#OD_AX').val(),
        od_pr: $('#OD_PR').val(),
        od_fr: $('#OD_FR').val(),
        od_add: $('#OD_ADD').val(),
        od_al: $('#OD_AL').val(),
        od_ak: $('#OD_AK').val(),
        od_ad: $('#OD_AD').val(),
        od_cct: $('#OD_CCT').val(),
        od_lt: $('#OD_LT').val(),
        od_vt: $('#OD_VT').val(),
        od_bc: $('#OD_BC').val(),
        os_va: $('#OS_VA').val(),
        os_sph: $('#OS_SPH').val(),
        os_cyl: $('#OS_CYL').val(),
        os_ax: $('#OS_AX').val(),
        os_pr: $('#OS_PR').val(),
        os_fr: $('#OS_FR').val(),
        os_add: $('#OS_ADD').val(),
        os_al: $('#OS_AL').val(),
        os_ak: $('#OS_AK').val(),
        os_ad: $('#OS_AD').val(),
        os_cct: $('#OS_CCT').val(),
        os_lt: $('#OS_LT').val(),
        os_vt: $('#OS_VT').val(),
        os_bc: $('#OS_BC').val()
    };

    const $submitBtn = $('#submitReport');
    setSubmitting($submitBtn, true);

    $.ajax({
        url: REPORT_INSERT_API,
        method: 'POST',
        data: formData,
        success: function(res) {
            setSubmitting($submitBtn, false);
            if (res.status === true) {
                alert('报告提交成功');
                // 可选：提交成功后重置表单（保留时间默认值）
                $('#name, #phone, #remark, #age, #sex, #dfh, #ot, #em, #PLAN, #PD').val('');
                $('#guestExtra input, #reportExtra input').val('');
                $('#name').focus();
            } else {
                showError('提交失败：' + (res.message || '未知错误'));
            }
        },
        error: function(xhr) {
            setSubmitting($submitBtn, false);
            showError('网络错误，请稍后重试');
        }
    });
}

// ==================== 折叠面板切换 ====================
function setupToggle(triggerId, panelId) {
    $(triggerId).on('click', function() {
        const $panel = $(panelId);
        $panel.slideToggle(200);
        $(this).find('i').toggleClass('bi-chevron-down bi-chevron-up');
    });
}

// ==================== 页面初始化 ====================
$(function() {
    // 初始化两个折叠面板
    setupToggle('#toggleGuest', '#guestExtra');
    setupToggle('#toggleReport', '#reportExtra');

    // 绑定提交按钮事件
    $('#submitReport').on('click', submitReport);

    // 可选：支持按回车键快速提交（在表单输入框内按回车）
    $('#guestSection input, #reportSection input').on('keypress', function(e) {
        if (e.which === 13) {
            e.preventDefault();
            submitReport();
        }
    });
});