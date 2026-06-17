$(document).ready(function () {
    $.ajax({
        url: api_order_detail,
        type: "GET",
        data: {order_id: order_id},
        success: function (res) {
            if (res.code === 0) {
                orders = jQuery.parseJSON(res.data[0].order)
                for (i in orders) {
                    content = '<tr>'
                    if (orders[i]['product'] === '镜框') {
                        content += '<td style="width: 9%"><span>' + orders[i]['product'] + '</span></td>'
                        content += '<td style="width: 9%"><span>' + orders[i]['brand'] + '</span></td>'
                        content += '<td style="width: 9%"><span>' + orders[i]['model'] + '</span></td>'
                        content += '<td colspan="7" style="width: 9%"></td>'
                        content += '<td style="width: 9%"><span>' + orders[i]['count'] + '</span></td>'
                    } else if (orders[i]['product'] === '镜片') {
                        content += '<td style="width: 9%"><span>' + orders[i]['product'] + '</span></td>'
                        content += '<td style="width: 9%"><span>' + orders[i]['brand'] + '</span></td>'
                        content += '<td style="width: 9%"><span>' + orders[i]['model'] + '</span></td>'
                        content += '<td style="width: 9%"><span>' + orders[i]['INDEX'] + '</span></td>'
                        content += '<td style="width: 9%"><span>' + orders[i]['Around'] + '</span></td>'
                        content += '<td style="width: 9%"><span>' + orders[i]['SPH'] + '</span></td>'
                        content += '<td style="width: 9%"><span>' + orders[i]['CYL'] + '</span></td>'
                        content += '<td style="width: 9%"><span>' + orders[i]['AX'] + '</span></td>'
                        content += '<td style="width: 9%"><span>' + orders[i]['Add'] + '</span></td>'
                        content += '<td style="width: 9%"><span>' + orders[i]['pd'] + '</span></td>'
                        content += '<td style="width: 9%"><span>' + orders[i]['count'] + '</span></td>'
                    }
                    content += '</tr>'
                    $('#order_content').append(content)
                }
            }
        }
    })
    // 获取二维码
    $("#get_qr_code").click(function () {
        $.ajax({
            url: api_order_qrcode,
            type: 'POST',
            data: $('#qr_code').serialize(),
            success: function (res) {
                if (res.code === 0) {
                    old_html = window.document.body.innerHTML
                    window.document.body.innerHTML = res.data
                    window.print();
                    window.document.body.innerHTML = old_html
                } else {
                    alert(res.msg)
                }
            },
        })
    });
    // 删除订单
    $("#delete").click(function () {
        $.ajax({
            url: api_order_delete,
            type: 'POST',
            data: $('#order_delete').serialize(),
            success: function (res) {
                alert(res.msg)
            },
        });
    });
});