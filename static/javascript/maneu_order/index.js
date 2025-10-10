function deleteBtn(obj) {
    if (confirm("您确定要删除吗？")) {
        $.ajax({
            url: api_delete,
            type: 'GET',
            data: {
                order_id: obj.alt,
            },
            success: function (res) {
                if (res.status === true) {
                    obj.parentElement.parentElement.parentElement.parentElement.remove()
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
    getList()
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
                "                <input type='button' class='col-12 btn btn-danger' onclick='deleteBtn(this)' value='删除' alt=" + res[i]['id'] + ">\n" +
                "            </div>\n" +
                "        </div>\n" +
                "        <div class='col-1'>\n" +
                "            <form method='GET' action='" + web_detail + "'>\n" +
                "                <input type='hidden' name='id' value=" + res[i]['id'] + ">\n" +
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
    function getList(){
        $.ajax({
            url: api_search,
            method: 'GET',
            data: {
                value: $("#value").val(),
                timeE: $("#timeE").val(),
                timeS: $("#timeS").val(),
            },
            success: function (res) {
                forList(res.content)
            }
        })
    }

    $('#search_button').click(function () {
        getList()
    })
})