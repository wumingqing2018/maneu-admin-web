$(document).ready(function () {
    $("#user_unfreeze").hide();
    $("#btn_freeze").click(function () {
        $.ajax({
            url: user_freeze,
            type: "POST",
            data: $("#user_freeze").serialize(),
            success: function (res) {
                $("#user_unfreeze").show();
                $("#user_freeze").hide();
                alert(res)
            }
        })
    })
    $("#btn_unfreeze").click(function () {
        $.ajax({
            url: user_unfreeze,
            type: "POST",
            data: $("#user_unfreeze").serialize(),
            success: function (res) {
                $("#user_freeze").show();
                $("#user_unfreeze").hide();
                alert(res)
            }
        })
    })
})
