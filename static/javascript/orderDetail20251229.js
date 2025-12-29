$(document).ready(function () {
    detail_order()

    $('#delete').click(function () {
        if (confirm("确定要删除记录吗？")) {
            $.ajax({
                url: order_delete,
                data: {
                    'order_id': order_id,
                    'guest_id': guest_id,
                    'report_id': report_id,
                },
                success: function (res) {

                }
            })
        } else {
            return false;
        }
    })

    $('#update').click(function () {
        if (confirm("确定要修改记录吗？")) {
            update_guest(function (data) {
                if (data.status === true) {
                    update_report(function (data) {
                        if (data.status === true) {
                            update_order(function (data) {
                                if (data.status === true) {
                                    alert('修改成功')
                                } else {
                                    alert(data.message)
                                }
                            })
                        } else {
                            alert(data.message)
                        }
                    })
                } else {
                    alert(data.message)
                }
            })
        } else {
            return false;
        }
    })


    function detail_order() {
        $.ajax({
            url: order_detail,
            data: {
                'order_id': order_id,
                'guest_id': guest_id,
                'report_id': report_id,
            },
            success: function (res) {
                if (res.status === true) {

                    guest = res.guest_id
                    if (guest.status === true) {
                        $('#time').val(guest.content.time)
                        $('#name').val(guest.content.name)
                        $('#phone').val(guest.content.phone)
                        $('#sex').val(guest.content.sex)
                        $('#age').val(guest.content.age)
                        $('#DFH').val(guest.content.dfh)
                        $('#EM').val(guest.content.em)
                        $('#OT').val(guest.content.ot)
                    }

                    report = res.report_id
                    if (report.status === true) {
                        console.log('report', report.content)
                        $('#time').val(report.content.time)
                        $('#PD').val(report.content.pd)
                        $('#PLAN').val(report.content.plan)

                        $('#OS_AX').val(report.content.os_ax)
                        $('#OS_AD').val(report.content.os_ad)
                        $('#OS_ADD').val(report.content.os_add)
                        $('#OS_AK').val(report.content.os_ak)
                        $('#OS_AL').val(report.content.os_al)
                        $('#OS_BC').val(report.content.os_bc)
                        $('#OS_CCT').val(report.content.os_cct)
                        $('#OS_CYL').val(report.content.os_cyl)
                        $('#OS_FR').val(report.content.os_fr)
                        $('#OS_LT').val(report.content.os_lt)
                        $('#OS_PR').val(report.content.os_pr)
                        $('#OS_SPH').val(report.content.os_sph)
                        $('#OS_VA').val(report.content.os_va)
                        $('#OS_VT').val(report.content.os_vt)

                        $('#OD_AX').val(report.content.od_ax)
                        $('#OD_AD').val(report.content.od_ad)
                        $('#OD_ADD').val(report.content.od_add)
                        $('#OD_AK').val(report.content.od_ak)
                        $('#OD_AL').val(report.content.od_al)
                        $('#OD_BC').val(report.content.od_bc)
                        $('#OD_CCT').val(report.content.od_cct)
                        $('#OD_CYL').val(report.content.od_cyl)
                        $('#OD_FR').val(report.content.od_fr)
                        $('#OD_LT').val(report.content.od_lt)
                        $('#OD_PR').val(report.content.od_pr)
                        $('#OD_SPH').val(report.content.od_sph)
                        $('#OD_VA').val(report.content.od_va)
                        $('#OD_VT').val(report.content.od_vt)
                    }

                    order = res.order_id
                    if (order.status === true) {
                        console.log('order', order.content)

                        $('#remark').val(order.content.remark)

                        for (var i = 0; i < order.content.content.length; i++) {
                            store = $(".store:eq(" + i + ")")
                            store.find(".arg10").val(order.content.content[i]['arg10'])
                            store.find(".arg11").val(order.content.content[i]['arg11'])
                            store.find(".arg12").val(order.content.content[i]['arg12'])
                            store.find(".arg13").val(order.content.content[i]['arg13'])
                            store.find(".arg14").val(order.content.content[i]['arg14'])
                        }
                    }
                }
            }
        })
    }


    function update_order(callback) {
        store = []
        $(".store").each(function () {
            data = {
                arg10: $(this).find(".arg10").val(),
                arg11: $(this).find(".arg11").val(),
                arg12: $(this).find(".arg12").val(),
                arg13: $(this).find(".arg13").val(),
                arg14: $(this).find(".arg14").val(),
            };
            store.push(data)
        })
        $.ajax({
            url: order_update,
            method: 'GET',
            data: {
                content: JSON.stringify(store),
                remark: $("#remark").val(),
                time: $("#time").val(),
                name: $("#name").val(),
                phone: $("#phone").val(),
                order_id: order_id,
            },
            success: function (res) {
                callback(res)
            },
            error: function () {
                callback({"status": false, 'message': 'order,网络出错'})
            }
        })
    }

    function update_guest(callback) {
        $.ajax({
            url: guest_update,
            method: 'GET',
            data: {
                guest_id: guest_id,
                remark: $("#remark").val(),
                time: $("#time").val(),
                name: $("#name").val(),
                phone: $("#phone").val(),
                age: $("#age").val(),
                sex: $("#sex").val(),
                DFH: $("#DFH").val(),
                OT: $("#OT").val(),
                EM: $("#EM").val(),
            },
            success: function (res) {
                callback(res)
            },
            error: function () {
                callback({"status": false, 'message': 'guest,网络出错'})
            }
        })
    }

    function update_report(callback) {
        content = {
            PLAN: $("#PLAN").val(),
            PD: $("#PD").val(),
            OD: {
                'VA': $("#OD_VA").val(),
                'SPH': $("#OD_SPH").val(),
                'CYL': $("#OD_CYL").val(),
                'AX': $("#OD_AX").val(),
                'PR': $("#OD_PR").val(),
                'FR': $("#OD_FR").val(),
                'ADD': $("#OD_ADD").val(),
                'AL': $("#OD_AL").val(),
                'AK': $("#OD_AK").val(),
                'AD': $("#OD_AD").val(),
                'CCT': $("#OD_CCT").val(),
                'LT': $("#OD_LT").val(),
                'VT': $("#OD_VT").val(),
                'BC': $("#OD_BC").val(),
            },
            OS: {
                'VA': $("#OS_VA").val(),
                'SPH': $("#OS_SPH").val(),
                'CYL': $("#OS_CYL").val(),
                'AX': $("#OS_AX").val(),
                'PR': $("#OS_PR").val(),
                'FR': $("#OS_FR").val(),
                'ADD': $("#OS_ADD").val(),
                'AL': $("#OS_AL").val(),
                'AK': $("#OS_AK").val(),
                'AD': $("#OS_AD").val(),
                'CCT': $("#OS_CCT").val(),
                'LT': $("#OS_LT").val(),
                'VT': $("#OS_VT").val(),
                'BC': $("#OS_BC").val(),
            },
        }
        $.ajax({
            url: report_update,
            method: "GET",
            data: {
                report_id: report_id,
                time: $("#time").val(),
                name: $("#name").val(),
                phone: $("#phone").val(),
                remark: $("#remark").val(),
                content: JSON.stringify(content)
            },
            success: function (res) {
                callback(res); // 第一个参数为null表示没有错误，第二个参数为请求的数据
            },
            error: function (res) {
                callback({"status": false, 'message': 'report,网络出错'})
            }
        })
    }
});
