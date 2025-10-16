function deleteBtn(obj) {
    if (confirm("您确定要删除吗？")) {
        $.ajax({
            url: api_delete,
            type: 'GET',
            data: {
                id: obj.alt,
            },
            success: function (res) {
                obj.parentElement.parentElement.parentElement.parentElement.remove()
            }
        })
    } else {
        return false;
    }
}

$(function () {
    var start = moment().subtract(29, 'days');
    var end = moment();

    function forList(res) {
        $('.body').empty();
        for (i in res) {
            $('.body').append(
                "<div>\n" +
                "    <div class='col-12 row'>\n" +
                "        <div class='col-2'>\n" +
                "            <p>" + res[i]['time'] + "</p>\n" +
                "        </div>\n" +
                "        <div class='col-1'>\n" +
                "            <p>" + res[i]['name'] + "</p>\n" +
                "        </div>\n" +
                "        <div class='col-1'>\n" +
                "            <p>" + res[i]['call'] + "</p>\n" +
                "        </div>\n" +
                "        <div class='col-6'>\n" +
                "            <p>" + res[i]['remark'] + "</p>\n" +
                "        </div>\n" +
                "        <div class='col-1'>\n" +
                "            <div class='input-group input-group-sm'>\n" +
                "                <input type='button' class='col-12 btn btn-danger' onclick='deleteBtn(this)' value='删除订单' alt=" + res[i]['id'] + ">\n" +
                "            </div>\n" +
                "        </div>\n" +
                "        <div class='col-1'>\n" +
                "            <form method='GET' action='" + api_detail + "'>\n" +
                "                <input type='hidden' name='id' value=" + res[i]['id'] + ">\n" +
                "                <div class='input-group input-group-sm'>\n" +
                "                    <input type='submit' class='col-12 btn btn-primary' value='查看订单'>\n" +
                "                </div>\n" +
                "            </form>\n" +
                "        </div>\n" +
                "    </div>\n" +
                "    <hr style='color: white'>\n" +
                "</div>\n"
            )
        }
    }

    function cb(start, end) {
        $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        $('#body').empty();
        $.ajax({
            url: api_index,
            data: {
                start: start.format('YYYY-MM-DD 00:00:00'),
                end: end.format('YYYY-MM-DD 23:59:59'),
            },
            success: function (res) {
                console.log(res)
                forList(res.content)
            },
        });
    }

    $('#search-value').keyup(function () {
        $.ajax({
            url: api_search,
            data: {
                text: $('#search-value').val()
            },
            success: function (res) {
                console.log(res)
                forList(res.content)
            }
        })
    })


    $('#reportrange').daterangepicker({
            startDate: start,
            endDate: end,
            ranges: {
                '今天': [moment(), moment()],
                '昨天': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                '七天内': [moment().subtract(6, 'days'), moment()],
                '三十天内': [moment().subtract(29, 'days'), moment()],
                '本月': [moment().startOf('month'), moment().endOf('month')],
                '上月': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            }
        },
        cb);

    cb(start, end);
});
