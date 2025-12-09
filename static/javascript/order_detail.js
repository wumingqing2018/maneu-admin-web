$(document).ready(function () {
    detail_order(function (data) {
        detail_report(function (data) {
            detail_guest(function (data) {
            })
        })
    })

    $('#delete').click(function () {
        if (confirm("确定要删除记录吗？")) {
            detail_order(function (data) {
                detail_report(function (data) {
                    detail_guest(function (data) {
                    })
                })
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


    function detail_order(callback) {
        $.ajax({
            url: order_detail,
            data: {
                'id': order_id
            },
            success: function (res) {
                $('#remark').val(res.content.remark)
                $('#name').val(res.content.name)
                $('#phone').val(res.content.phone)
                $('#time').val(res.content.time)

                console.log('order', res.content.content)

                for (var i = 0; i < res.content.content.length; i++) {
                    store = $(".store:eq(" + i + ")")
                    store.find(".arg10").val(res.content.content[i]['arg10'])
                    store.find(".arg11").val(res.content.content[i]['arg11'])
                    store.find(".arg12").val(res.content.content[i]['arg12'])
                    store.find(".arg13").val(res.content.content[i]['arg13'])
                    store.find(".arg14").val(res.content.content[i]['arg14'])
                }

                callback(true); // 第一个参数为null表示没有错误，第二个参数为请求的数据
            },
            error: function (res) {
                alert(res)
                callback(false); // 第一个参数为null表示没有错误，第二个参数为请求的数据
            }
        })
    }

    function detail_guest(callback) {
        $.ajax({
            url: guest_detail,
            data: {
                'id': guest_id
            },
            success: function (res) {
                console.log('guest', res.content)
                content = res.content
                $('#name').val(content.name)
                $('#call').val(content.phone)
                $('#age').val(content.age)
                $('#DFH').val(content.dfh)
                $('#EM').val(content.em)
                $('#OT').val(content.ot)
                $('#sex').val(content.sex)
                callback(true); // 第一个参数为null表示没有错误，第二个参数为请求的数据
            },
            error: function (res) {
                alert(res)
                callback(false); // 第一个参数为null表示没有错误，第二个参数为请求的数据
            }
        })
    }

    function detail_report(callback) {
        $.ajax({
            url: report_detail,
            data: {
                'id': report_id
            },
            success: function (res) {
                console.log('report', res)
                content = res.content
                $('#time').val(content.time)
                $('#PD').val(content.pd)
                $('#PLAN').val(content.plan)

                $('#OS_AX').val(content.os_ax)
                $('#OS_AD').val(content.os_ad)
                $('#OS_ADD').val(content.os_add)
                $('#OS_AK').val(content.os_ak)
                $('#OS_AL').val(content.os_al)
                $('#OS_BC').val(content.os_bc)
                $('#OS_CCT').val(content.os_cct)
                $('#OS_CYL').val(content.os_cyl)
                $('#OS_FR').val(content.os_fr)
                $('#OS_LT').val(content.os_lt)
                $('#OS_PR').val(content.os_pr)
                $('#OS_SPH').val(content.os_sph)
                $('#OS_VA').val(content.os_va)
                $('#OS_VT').val(content.os_vt)

                $('#OD_AX').val(content.od_ax)
                $('#OD_AD').val(content.od_ad)
                $('#OD_ADD').val(content.od_add)
                $('#OD_AK').val(content.od_ak)
                $('#OD_AL').val(content.od_al)
                $('#OD_BC').val(content.od_bc)
                $('#OD_CCT').val(content.od_cct)
                $('#OD_CYL').val(content.od_cyl)
                $('#OD_FR').val(content.od_fr)
                $('#OD_LT').val(content.od_lt)
                $('#OD_PR').val(content.od_pr)
                $('#OD_SPH').val(content.od_sph)
                $('#OD_VA').val(content.od_va)
                $('#OD_VT').val(content.od_vt)
                callback(true); // 第一个参数为null表示没有错误，第二个参数为请求的数据
            },
            error: function (res) {
                alert(res)
                callback(false); // 第一个参数为null表示没有错误，第二个参数为请求的数据
            }
        })
    }

    function delete_order(callback) {
        $.ajax({
            url: order_delete,
            data: {
                'id': order_id
            },
            success: function (res) {
                callback(res)
            },
            error: function () {
                callback({"status": false, 'message': 'order,网络出错'})
            }
        })
    }

    function delete_report(callback) {
        $.ajax({
            url: report_delete,
            data: {
                'id': report_id
            },
            success: function (res) {
                callback(res)
            },
            error: function () {
                callback({"status": false, 'message': 'order,网络出错'})
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
