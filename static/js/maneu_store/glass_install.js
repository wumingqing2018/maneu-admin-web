$(document).ready(
    $('#btn_glass_insert').click(function () {
        $.ajax({
            url: api_glass_insert,
            type: "POST",
            data: $('#glass_insert').serialize(),
            success: function (res) {
                alert(res['msg'])
            }
        })
    }),
)
