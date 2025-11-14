$(document).ready(function () {
    $('#insert').click(function () {
        $.ajax({
            url: report_api,
            method: 'GET',
            data: {
                remark: $("#remark").val(),
                time: $("#time").val(),
                name: $("#name").val(),
                phone: $("#phone").val(),


                age: $("#age").val(),
                sex: $("#sex").val(),
                DFH: $("#DFH").val(),
                OT: $("#OT").val(),
                EM: $("#EM").val(),


                plan: $("#PLAN").val(),
                pd: $("#PD").val(),
                od_va: $("#OD_VA").val(),
                od_sph: $("#OD_SPH").val(),
                od_cyl: $("#OD_CYL").val(),
                od_ax: $("#OD_AX").val(),
                od_pr: $("#OD_PR").val(),
                od_fr: $("#OD_FR").val(),
                od_add: $("#OD_ADD").val(),
                od_al: $("#OD_AL").val(),
                od_ak: $("#OD_AK").val(),
                od_ad: $("#OD_AD").val(),
                od_cct: $("#OD_CCT").val(),
                od_lt: $("#OD_LT").val(),
                od_vt: $("#OD_VT").val(),
                od_bc: $("#OD_BC").val(),
                os_va: $("#OS_VA").val(),
                os_sph: $("#OS_SPH").val(),
                os_cyl: $("#OS_CYL").val(),
                os_ax: $("#OS_AX").val(),
                os_pr: $("#OS_PR").val(),
                os_fr: $("#OS_FR").val(),
                os_add: $("#OS_ADD").val(),
                os_al: $("#OS_AL").val(),
                os_ak: $("#OS_AK").val(),
                os_ad: $("#OS_AD").val(),
                os_cct: $("#OS_CCT").val(),
                os_lt: $("#OS_LT").val(),
                os_vt: $("#OS_VT").val(),
                os_bc: $("#OS_BC").val(),
            },
            success: function (res) {
                if (res.status === true) {
                    alert('提交成功')
                } else {
                    alert('提交失败，错误信息：' + res.message)
                }
            },
            error: function (res) {
                callback({'status': false, 'message': '请求出错请刷新页面'}); // 第一个参数为null表示没有错误，第二个参数为请求的数据
            }
        })
    });
});
