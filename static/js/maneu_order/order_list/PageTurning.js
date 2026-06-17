$(document).ready(function () {
    $("#down").click(function () {
        min = min + 100
        max = max + 100
        $.ajax({
            url: api_order_list,
            type: 'GET',
            data: {'min': min, 'max': max},
            success: function (res) {
                if (res.code === 0) {
                    if (res.msg.length === 100) {
                        alert(res.msg.length)
                        $("#up").show()
                    } else {
                        $("#down").hide()
                    }
                }
            }
        })
    })
    $("#up").click(function () {
        alert('1')
        min = min - 10
        max = max - 10
        $.ajax({
            url: api_order_list,
            type: 'GET',
            data: {'min': min, 'max': max},
            success: function (res) {
            }
        })
    })
})
