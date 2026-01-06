function deleteBtn(obj) {
    if (confirm("您确定要删除吗？")) {
        $.ajax({
            url: api_delete,
            type: 'GET',
            data: {
                guest_id: obj.dataset.guest_id,
                order_id: obj.dataset.order_id,
                report_id: obj.dataset.report_id,
            },
            success: function (res) {
                console.log(res)
                if (res.status === true) {
                    obj.parentElement.parentElement.parentElement.parentElement.parentElement.remove()
                } else {
                    alert(res.message)
                }
            },
        })

    } else {
        return false;
    }
}


$(document).ready(function () {
    $.ajax({
        url: search_time,
        method: 'GET',
        data: {
            timeE: $("#timeE").val(),
            timeS: $("#timeS").val(),
        },
        success: function (res) {
            console.log(res)
            forList(res.content)
        }
    })

    $('#search_time').click(function () {
        $.ajax({
            url: search_time,
            method: 'GET',
            data: {
                timeE: $("#timeE").val(),
                timeS: $("#timeS").val(),
            },
            success: function (res) {
                console.log(res)
                forList(res.content)
            }
        })
    })

    $('#search_data').click(function () {
        $.ajax({
            url: search_data,
            method: 'GET',
            data: {
                value: $("#value").val(),
            },
            success: function (res) {
                console.log(res)
                forList(res.content)
            }
        })
    })

    function forList(res) {
        $('#body').empty();
        for (i in res) {
            $('#body').append(
                "<div>\n" +
                "    <div class='col-12 row'>\n" +
                "        <div class='col-2'>\n" +
                "            <p>" + res[i]['time'] + "</p>\n" +
                "        </div>\n" +
                "        <div class='col-1'>\n" +
                "            <p>" + res[i]['name'] + "</p>\n" +
                "        </div>\n" +
                "        <div class='col-1'>\n" +
                "            <p>" + res[i]['phone'] + "</p>\n" +
                "        </div>\n" +
                "        <div class='col-6'>\n" +
                "            <p>" + res[i]['remark'] + "</p>\n" +
                "        </div>\n" +
                "        <div class='col-1'>\n" +
                "            <div class='input-group input-group-sm'>\n" +
                "                <input type='button' class='col-12 btn btn-danger' onclick='deleteBtn(this)' value='删除' data-guest_id=" + res[i]['guest_id'] + " data-report_id=" + res[i]['report_id'] + " data-order_id=" + res[i]['id'] + " >\n" +
                "            </div>\n" +
                "        </div>\n" +
                "        <div class='col-1'>\n" +
                "            <form method='GET' action='" + api_detail + "'>\n" +
                "                <input type='hidden' name='order_id' value=" + res[i]['id'] + ">\n" +
                "                <input type='hidden' name='guest_id' value=" + res[i]['guest_id'] + ">\n" +
                "                <input type='hidden' name='report_id' value=" + res[i]['report_id'] + ">\n" +
                "                <div class='input-group input-group-sm'>\n" +
                "                    <input type='submit' class='col-12 btn btn-primary' value='查看'>\n" +
                "                </div>\n" +
                "            </form>\n" +
                "        </div>\n" +
                "    </div>\n" +
                "    <hr style='color: white'>\n" +
                "</div>\n"
            )
        }
    }
})