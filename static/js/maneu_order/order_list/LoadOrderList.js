$(document).ready(function () {
    $.ajax({
        url: api_order_list,
        type: 'GET',
        data: {'min': min},
        success: function (res) {
            console.log(res)
        }
    })
})